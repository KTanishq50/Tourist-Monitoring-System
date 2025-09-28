from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TouristProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class TouristProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TouristProfile
        fields = ["user", "aadhaar_number", "pan_number", "days_of_stay", "verified"]


class TouristProfileCreateSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = TouristProfile
        fields = ["username", "password", "aadhaar_number", "pan_number", "days_of_stay"]

    def create(self, validated_data):
        username = validated_data.pop("username")
        password = validated_data.pop("password")

        
        user = User.objects.create_user(username=username, password=password)

        
        profile = TouristProfile.objects.create(user=user, **validated_data)
        return profile
