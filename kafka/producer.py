from confluent_kafka import Producer
import time

bootstrap_servers = "broker1:9092,broker2:9093,broker3:9094"
conf = {
    'bootstrap.servers': bootstrap_servers,
    'client.id': 'python-producer-example'
}
producer = Producer(conf)
topic = "test-topic"

for i in range(10):
    message = f"Hello Kafka! Message #{i}"
    producer.produce(
        topic=topic,
        key=str(i),
        value=message,
    )
    #For readability
    time.sleep(0.2)

producer.flush()