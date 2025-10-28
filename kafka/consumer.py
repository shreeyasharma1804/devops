from confluent_kafka import Consumer, KafkaException, KafkaError, TopicPartition
import time

conf = {
    'bootstrap.servers': 'localhost:19092,localhost:19093,localhost:19094',
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['test-topic'])

# To subscribe from a given partition
# topic = 'test-topic'
# partition = 0

# consumer.subscribe([TopicPartition(topic, partition)])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                raise KafkaException(msg.error())
        else:
            print(f"Received message: {msg.value().decode('utf-8')} from partition {msg.partition()}")
        time.sleep(1)

finally:
    consumer.close()
