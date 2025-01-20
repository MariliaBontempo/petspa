from confluent_kafka.admin import AdminClient, NewTopic
import os
import time

def create_topics():
    """
    Creates required Kafka topics if they don't exist
    """
    print("Starting Kafka topic creation...")
    
    # Topics to be created with their configs
    topics = {
        'magic-links.created': {
            'num_partitions': 1,
            'replication_factor': 1
        }
    }

    # Connect to Kafka
    admin_client = AdminClient({
        'bootstrap.servers': os.getenv('KAFKA_BROKERS', 'kafka:9092')
    })

    # Create topics
    new_topics = [
        NewTopic(
            topic,
            num_partitions=config['num_partitions'],
            replication_factor=config['replication_factor']
        ) for topic, config in topics.items()
    ]

if __name__ == "__main__":
    create_topics()
