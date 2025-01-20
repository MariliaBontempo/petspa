import graphene
from .registry import EventRegistry
from .repositories import KafkaEventRepository

class DynamicEventMutation(graphene.Mutation):
    class Arguments:
        event_type = graphene.String(required=True)
        input = graphene.JSONString(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(root, info, event_type: str, input: dict):
        try:
            # Obtém o handler do registro
            handler_class = EventRegistry.get_handler(event_type)
            if not handler_class:
                return DynamicEventMutation(
                    success=False, 
                    message=f"Unknown event type: {event_type}"
                )

            # Cria e executa o handler
            handler = handler_class()
            event = handler.handle(input)

            # Publica o evento
            repository = KafkaEventRepository()
            success = repository.publish(event)

            return DynamicEventMutation(success=success)
        except Exception as e:
            return DynamicEventMutation(success=False, message=str(e))

class EventBrokerMutation(graphene.ObjectType):
    publish_event = DynamicEventMutation.Field() 