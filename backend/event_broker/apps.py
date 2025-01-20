from django.apps import AppConfig
from django.conf import settings


class EventBrokerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'event_broker'

    def ready(self):
        from .events import MagicLinkHandler
        from .registry import EventRegistry
        
        # Registra os handlers
        EventRegistry.register('magic_link', MagicLinkHandler)
