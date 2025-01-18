import graphene
from healthy_check.schema import Query as HealthCheckQuery
from accounts.schema import Query as UserQuery, Mutation as UserMutation

class Query(UserQuery, HealthCheckQuery, graphene.ObjectType):
    pass

class Mutation(UserMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation) 