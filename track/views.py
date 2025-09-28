import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from .models import UserLocation, UserLocationHistory


def update_location(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            lat = float(data.get("latitude"))
            lon = float(data.get("longitude"))
        except Exception:
            return JsonResponse({"error": "invalid payload"}, status=400)

        
        UserLocation.objects.update_or_create(
            user=request.user,
            defaults={"latitude": lat, "longitude": lon, "updated_at": timezone.now()}
        )

     
        ulh, created = UserLocationHistory.objects.get_or_create(user=request.user)
        ulh.coords.append({"lat": lat, "lon": lon})
        ulh.save(update_fields=["coords", "updated_at"])

        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "invalid request"}, status=400)


def authority_map(request):
    return render(request, "track/track_users.html")


def get_all_locations(request):
    locations = list(UserLocation.objects.select_related("user").values(
        "user__username", "latitude", "longitude", "anomalous"
    ))
    return JsonResponse({"locations": locations})
