from confluent_kafka import Producer
import time

bootstrap_servers = "localhost:19092,localhost:19093,localhost:19094"
conf = {
    'bootstrap.servers': bootstrap_servers,
    'client.id': 'python-producer-example'
}
producer = Producer(conf)
topic = "test-topic"

for i in range(10, 20):
    message = f"Hello Kafka! Message #{i}"
    print(message)
    producer.produce(
        topic=topic,
        key=str(i),
        value=message,
    )
    #For readability
    time.sleep(0.2)

producer.flush()