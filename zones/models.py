from django.db import models
from django.contrib.auth.models import User

class Zone(models.Model):
    ZONE_TYPES = [
        ("safe", "Safe Zone"),
        ("unsafe", "Unsafe Zone"),
        ("restricted", "Restricted Zone"),
    ]

    name = models.CharField(max_length=100, unique=True)
    zone_type = models.CharField(max_length=20, choices=ZONE_TYPES, default="unsafe")
    geom = models.JSONField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def color(self):
        return {
            "safe": "#00FF00",
            "unsafe": "#FF0000",
            "restricted": "#FFFF00",
        }.get(self.zone_type, "#FF0000")

    def __str__(self):
        return self.name

