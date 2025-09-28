# track/apps.py
from django.apps import AppConfig

class TrackConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "track"

    def ready(self):
        import track.signals
