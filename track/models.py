from django.db import models
from django.contrib.auth.models import User

class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)
    anomalous = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - ({self.latitude}, {self.longitude})"


class UserLocationHistory(models.Model):
    
    #Uses JSONField to store list of {"lat": ..., "lon": ...}.
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="location_history")
    coords = models.JSONField(default=list, blank=True)  # list of {"lat":..., "lon":...}
    eligible_for_ml = models.BooleanField(default=False)
    consumed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {len(self.coords)} points"


class AnomalyAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True)
    details = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Alert {self.user.username} @ {self.timestamp.isoformat()}"
