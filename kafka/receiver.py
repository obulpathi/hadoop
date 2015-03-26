from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer

endpoint = "172.17.0.9:9092"
kafka = KafkaClient(endpoint)

print("After connecting to kafka")

consumer = SimpleConsumer(kafka, "my-group", "test")

for message in consumer:
    print(message)
