from django.db import models
from django.contrib.auth.models import User

class TouristProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aadhaar_number = models.CharField(max_length=12, unique=True)
    pan_number = models.CharField(max_length=10, unique=True)
    days_of_stay = models.PositiveIntegerField()
    verified = models.BooleanField(default=False)

    
    qr_code = models.ImageField(upload_to="qrcodes/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Verified: {self.verified}"
