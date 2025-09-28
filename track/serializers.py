from rest_framework import serializers
from .models import UserLocation, UserLocationHistory, AnomalyAlert


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = ["latitude", "longitude", "updated_at", "anomalous"]


class UserLocationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocationHistory
        fields = ["coords", "eligible_for_ml", "consumed", "updated_at"]


class AnomalyAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnomalyAlert
        fields = ["timestamp", "score", "details"]
