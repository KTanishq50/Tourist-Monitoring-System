from django.urls import path
from . import views

app_name = "routing"





urlpatterns = [
    path("map-input/", views.map_input, name="map_input"),
    
    
]
