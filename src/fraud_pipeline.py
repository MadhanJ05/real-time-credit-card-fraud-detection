
import json
from kafka import KafkaConsumer, KafkaProducer
from feature_engineering import FeatureEngineer
from mongodb_storage import MongoDBStorage

class FraudDetectionPipeline:
    def __init__(self, kafka_config, mongodb_connection, group_id='fraud-pipeline-group'):
        # Kafka consumer
        self.consumer = KafkaConsumer(
            'transactions',
            bootstrap_servers=kafka_config['bootstrap_servers'],
            security_protocol='SASL_SSL',
            sasl_mechanism='PLAIN',
            sasl_plain_username=kafka_config['api_key'],
            sasl_plain_password=kafka_config['api_secret'],
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset='latest',
            group_id=group_id,
            consumer_timeout_ms=15000
        )
        
        # Kafka producer (for fraud alerts)
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_config['bootstrap_servers'],
            security_protocol='SASL_SSL',
            sasl_mechanism='PLAIN',
            sasl_plain_username=kafka_config['api_key'],
            sasl_plain_password=kafka_config['api_secret'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        # Feature engineer
        self.fe = FeatureEngineer()
        
        # MongoDB storage
        self.storage = MongoDBStorage(mongodb_connection)
        
        # Fraud detection thresholds
        self.thresholds = {
            'velocity_6h': 5,
            'avg_spend_diff': 500,
            'distance_speed': 1000,
            'odd_hour_start': 2,
            'odd_hour_end': 5
        }
    
    def detect_fraud(self, transaction):
        """Apply rule-based fraud detection"""
        fraud_reasons = []
        
        if transaction.get('velocity_6h', 0) > self.thresholds['velocity_6h']:
            fraud_reasons.append(f"High velocity: {transaction['velocity_6h']} txns in 6h")
        
        if transaction.get('avg_spend_diff', 0) > self.thresholds['avg_spend_diff']:
            fraud_reasons.append(f"Amount anomaly: ${transaction['avg_spend_diff']} above average")
        
        if transaction.get('distance_speed', 0) > self.thresholds['distance_speed']:
            fraud_reasons.append(f"Impossible travel: {transaction['distance_speed']:.0f} km/h")
        
        try:
            hour = int(transaction['timestamp'].split(' ')[1].split(':')[0])
            if self.thresholds['odd_hour_start'] <= hour <= self.thresholds['odd_hour_end']:
                fraud_reasons.append(f"Odd hour transaction: {hour}:00")
        except:
            pass
        
        return fraud_reasons
    
    def process_transaction(self, transaction):
        """Process a single transaction"""
        enriched = self.fe.add_features(transaction)
        
        fraud_reasons = self.detect_fraud(enriched)
        enriched['fraud_reasons'] = fraud_reasons
        enriched['predicted_fraud'] = len(fraud_reasons) > 0
        
        self.storage.store_transaction(enriched)
        
        if enriched['predicted_fraud']:
            self.producer.send('fraud-alerts', value=enriched)
            self.producer.flush()
            self.storage.store_fraud_alert(enriched)
        
        return enriched
    
    def run(self, max_messages=None):
        """Run the pipeline"""
        print("Starting fraud detection pipeline...")
        count = 0
        
        for message in self.consumer:
            transaction = message.value
            result = self.process_transaction(transaction)
            
            status = "🚨 FRAUD" if result['predicted_fraud'] else "✅ OK"
            print(f"{status} | ${result['amount']:.2f} | {result['first_name']} {result['last_name']}")
            
            if result['predicted_fraud']:
                for reason in result['fraud_reasons']:
                    print(f"    → {reason}")
            
            count += 1
            if max_messages and count >= max_messages:
                break
        
        print(f"\nProcessed {count} transactions")
        print(f"Total in DB: {self.storage.get_transaction_count()}")
        print(f"Fraud alerts: {self.storage.get_fraud_count()}")
    
    def close(self):
        self.consumer.close()
        self.producer.close()
