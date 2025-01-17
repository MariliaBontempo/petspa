import graphene
from accounts.schema import Mutation as AccountsMutation
from healthy_check.schema import Query as HealthCheckQuery

class Query(HealthCheckQuery, graphene.ObjectType):
    pass

class Mutation(AccountsMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation) 