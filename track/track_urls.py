
from django.urls import path
from . import views

app_name = "track"

urlpatterns = [
    path("api/update-location/", views.update_location, name="update_location"),
    path("authority-map/", views.authority_map, name="authority_map"),
    path("api/get-locations/", views.get_all_locations, name="get_locations"),
]

