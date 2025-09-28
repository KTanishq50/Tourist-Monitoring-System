from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from zones.views import ZoneViewSet
from . import views  

router = DefaultRouter()
router.register(r'zones', ZoneViewSet)

urlpatterns = [
    path('', views.landing_page, name='landing'),  
    path('authority/', views.authority_home, name='authority_home'),  

    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),     
    path('zones/', include('zones.zones_urls')),        
    path("track/", include("track.track_urls")),
    path("routing/", include("routing.routing_urls")),
    path("user/", include("user.user_urls")),
    path("blockchain/", include("blockchain.blockchain_urls")),
    path("api/mobile/", include("mobile_api.mobile_urls")),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
