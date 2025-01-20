import graphene
from graphene_django import DjangoObjectType
from .models import User
import logging

logger = logging.getLogger('accounts')

# Define GraphQL type for User model
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'email', 'user_type')

class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    
    def resolve_me(self, info):
        user = info.context.user
        return user if user.is_authenticated else None