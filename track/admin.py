# track/admin.py
from django.contrib import admin
from .models import UserLocation, UserLocationHistory, AnomalyAlert
import json

class UserLocationHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "num_coords", "eligible_for_ml", "consumed", "updated_at")
    
    def num_coords(self, obj):
        return len(obj.coords)
    num_coords.short_description = "Number of Points"

admin.site.register(UserLocation)
admin.site.register(UserLocationHistory, UserLocationHistoryAdmin)
admin.site.register(AnomalyAlert)
