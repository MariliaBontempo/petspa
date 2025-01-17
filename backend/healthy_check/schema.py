import graphene

class HealthCheckType(graphene.ObjectType):
    status = graphene.String()

class Query(graphene.ObjectType):
    health_check = graphene.Field(HealthCheckType)

    def resolve_health_check(self, info):
        return HealthCheckType(status='ok') 