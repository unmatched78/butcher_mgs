# communications/apps.py
from django.apps import AppConfig

class CommunicationsConfig(AppConfig):
    name = 'communications'

    def ready(self):
        import communications.signals  # Import signals