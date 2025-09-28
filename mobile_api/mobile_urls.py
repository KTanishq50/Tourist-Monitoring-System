from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_mobile, name="mobile-register"),
    path("login/", views.login_mobile, name="mobile-login"),
    path("qr/<int:user_id>/", views.qr_mobile, name="mobile-qr"),
    path("location/", views.location_mobile, name="mobile-location"),
]
