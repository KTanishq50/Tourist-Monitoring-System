# urls.py
from django.urls import path
from . import views

app_name = "blockchain"

urlpatterns = [
    path("blockchain_dashboard/", views.blockchain_dashboard, name="blockchain_dashboard"),
    path("verify/<str:tourist_id>/", views.verify_qr, name="verify-qr"),


]
