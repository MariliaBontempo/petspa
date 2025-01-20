from abc import ABC, abstractmethod
import json
from confluent_kafka import Producer
from .events import Event

class EventRepository(ABC):
    @abstractmethod
    def publish(self, event: Event) -> bool:
        pass

class KafkaEventRepository(EventRepository):
    def __init__(self):
        self.producer = Producer({'bootstrap.servers': 'kafka:9092'})

    def publish(self, event: Event) -> bool:
        try:
            self.producer.produce(
                event.topic,
                value=json.dumps(event.payload).encode('utf-8')
            )
            self.producer.flush()
            return True
        except Exception as e:
            print(f"Error publishing event: {e}")
            return False