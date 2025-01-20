from typing import Dict, Type
from .events import EventHandler

class EventRegistry:
    _handlers: Dict[str, Type[EventHandler]] = {}

    @classmethod
    def register(cls, name: str, handler: Type[EventHandler]):
        cls._handlers[name] = handler

    @classmethod
    def get_handler(cls, name: str) -> Type[EventHandler]:
        return cls._handlers.get(name)

    @classmethod
    def get_all_handlers(cls):
        return cls._handlers

# Register the handlers
EventRegistry.register('magic_link', MagicLinkHandler) 