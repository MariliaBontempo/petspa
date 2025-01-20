import graphene
from accounts.schema import Query as AccountsQuery

class Query(AccountsQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query) 