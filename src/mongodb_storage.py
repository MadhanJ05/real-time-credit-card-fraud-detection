
from pymongo import MongoClient
from datetime import datetime

class MongoDBStorage:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client["fraud_detection"]
        self.transactions = self.db["transactions"]
        self.fraud_alerts = self.db["fraud_alerts"]
    
    def store_transaction(self, transaction):
        """Store a transaction in MongoDB"""
        # Make a copy to avoid modifying original
        txn_copy = transaction.copy()
        txn_copy["stored_at"] = datetime.now()
        result = self.transactions.insert_one(txn_copy)
        return result.inserted_id
    
    def store_fraud_alert(self, transaction):
        """Store a fraud alert separately"""
        # Make a copy to avoid modifying original
        txn_copy = transaction.copy()
        txn_copy["alerted_at"] = datetime.now()
        result = self.fraud_alerts.insert_one(txn_copy)
        return result.inserted_id
    
    def get_recent_transactions(self, limit=10):
        """Get recent transactions"""
        return list(self.transactions.find().sort("stored_at", -1).limit(limit))
    
    def get_fraud_alerts(self, limit=10):
        """Get recent fraud alerts"""
        return list(self.fraud_alerts.find().sort("alerted_at", -1).limit(limit))
    
    def get_fraud_count(self):
        """Get total fraud count"""
        return self.fraud_alerts.count_documents({})
    
    def get_transaction_count(self):
        """Get total transaction count"""
        return self.transactions.count_documents({})
