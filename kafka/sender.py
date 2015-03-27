import logging
from datetime import datetime

from kafka.client import KafkaClient
from kafka.producer import SimpleProducer

logging.basicConfig()

endpoint = "172.17.0.5:9092"
client =  KafkaClient(endpoint)

producer = SimpleProducer(client)

producer.send_messages("topic", "This is message sent from python client " + str(datetime.now().time()))
