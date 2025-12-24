
import json
from kafka import KafkaConsumer

class TransactionConsumer:
    def __init__(self, bootstrap_servers, api_key, api_secret, topic):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            security_protocol='SASL_SSL',
            sasl_mechanism='PLAIN',
            sasl_plain_username=api_key,
            sasl_plain_password=api_secret,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset='earliest',
            group_id='fraud-detection-group'
        )
    
    def consume(self, max_messages=None):
        """Consume messages from Kafka"""
        count = 0
        for message in self.consumer:
            transaction = message.value
            yield transaction
            count += 1
            if max_messages and count >= max_messages:
                break
    
    def close(self):
        self.consumer.close()
