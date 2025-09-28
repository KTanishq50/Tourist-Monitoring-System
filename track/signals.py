from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserLocation, UserLocationHistory, AnomalyAlert
from .ml_utils.model_io import load_model
from .ml_model.features import extract_features

WINDOW_SIZE = getattr(settings, "ML_WINDOW_SIZE", 100)
THRESHOLD = getattr(settings, "ML_ANOMALY_THRESHOLD", 0.8)


model = load_model()


@receiver(post_save, sender=UserLocation)
def process_location(sender, instance, **kwargs):
    """
    Triggered whenever a UserLocation is updated.
    Updates the JSONField history and runs ML if enough points.
    """
    ulh, created = UserLocationHistory.objects.get_or_create(user=instance.user)

    ulh.coords.append({"lat": instance.latitude, "lon": instance.longitude})


    if len(ulh.coords) >= WINDOW_SIZE and not ulh.consumed:
        ulh.eligible_for_ml = True

        recent_coords = ulh.coords[-WINDOW_SIZE:]
        features = extract_features(recent_coords, instance.user)

    
        score = model.decision_function([features])[0]

        if score > THRESHOLD:
          
            instance.anomalous = True
            instance.save(update_fields=["anomalous"])
            AnomalyAlert.objects.create(
                user=instance.user,
                score=score,
                details={"features": features}
            )
        else:
            instance.anomalous = False
            instance.save(update_fields=["anomalous"])

        
        ulh.consumed = True
        ulh.eligible_for_ml = False

    ulh.save(update_fields=["coords", "eligible_for_ml", "consumed", "updated_at"])
