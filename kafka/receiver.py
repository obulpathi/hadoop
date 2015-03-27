from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer

endpoint = "172.17.0.5:9092"
kafka = KafkaClient(endpoint)

print("After connecting to kafka")

consumer = SimpleConsumer(kafka, "group", "topic")

for message in consumer:
    print(message)
