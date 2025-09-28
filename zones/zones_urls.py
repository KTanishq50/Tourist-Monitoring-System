from django.urls import path
from . import views


app_name = "zones"

urlpatterns = [
    path('zones_dashboard/', views.zones_dashboard, name='zones_dashboard'),
]
