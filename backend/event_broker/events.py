from dataclasses import dataclass
from typing import Any, Dict, Type
from abc import ABC
import graphene
from django.contrib.auth.tokens import default_token_generator
from django.utils.crypto import get_random_string

@dataclass
class Event:
    topic: str
    payload: dict

class EventHandler(ABC):
    @property
    def input_type(self) -> Type[graphene.InputObjectType]:
        raise NotImplementedError
    
    def handle(self, input_data: Dict) -> Event:
        raise NotImplementedError

class MagicLinkHandler(EventHandler):
    @property
    def input_type(self):
        class MagicLinkInput(graphene.InputObjectType):
            email = graphene.String(required=True)
            user_type = graphene.String(required=True)
        return MagicLinkInput

    def handle(self, input_data: Dict) -> Event:
        return Event(
            topic="magic-links.created",
            payload={
                "email": input_data["email"],
                "userType": input_data["user_type"],
                "token": generate_token()
            }
        )

def generate_token() -> str:
    return get_random_string(32) 