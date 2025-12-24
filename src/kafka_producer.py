
import json
import time
import random
from kafka import KafkaProducer
from generators import generate_cardholder, generate_merchant
from transaction_generator import generate_transaction
from history_tracker import TransactionHistory
from fraud_generator import generate_fraud_transaction

class TransactionProducer:
    def __init__(self, bootstrap_servers, api_key, api_secret):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            security_protocol='SASL_SSL',
            sasl_mechanism='PLAIN',
            sasl_plain_username=api_key,
            sasl_plain_password=api_secret,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.history = TransactionHistory()
        self.cardholders = [generate_cardholder() for _ in range(100)]
    
    def send_transaction(self, topic, transaction):
        """Send a transaction to Kafka"""
        self.producer.send(topic, value=transaction)
        self.producer.flush()
    
    def generate_and_send(self, topic, fraud_ratio=0.05):
        """Generate a transaction and send to Kafka"""
        cardholder = random.choice(self.cardholders)
        
        # Decide if fraud or normal (5% fraud by default)
        if random.random() < fraud_ratio:
            transaction = generate_fraud_transaction(cardholder, self.history)
        else:
            merchant = generate_merchant()
            transaction = generate_transaction(cardholder, merchant)
            transaction["fraud_type"] = None
        
        # Add to history
        self.history.add_transaction(cardholder["cc_num"], transaction)
        
        # Send to Kafka
        self.send_transaction(topic, transaction)
        
        return transaction
