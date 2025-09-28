from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Zone
from .serializers import ZoneSerializer



class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    permission_classes = [IsAuthenticated]




def zones_dashboard(request):
    
    zones = Zone.objects.all()


    from django.core.serializers import serialize
    zones_json = serialize("json", zones)

    return render(request, "zones/dashboard.html", {
        "zones_json": zones_json
    })
