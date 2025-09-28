from rest_framework import serializers
from .models import Zone

class ZoneSerializer(serializers.ModelSerializer):
    color = serializers.ReadOnlyField()  

    class Meta:
        model = Zone
        fields = ["id", "name", "zone_type", "geom", "author", "created_at", "updated_at", "color"]
