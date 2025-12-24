
from datetime import datetime, timedelta
from collections import defaultdict

class TransactionHistory:
    def __init__(self):
        # Store transactions per cardholder
        self.transactions = defaultdict(list)
    
    def add_transaction(self, cc_num, transaction):
        """Add a transaction to history"""
        self.transactions[cc_num].append({
            "timestamp": transaction["timestamp"],
            "unix_time": transaction["unix_time"],
            "amount": transaction["amount"],
            "merchant_lat": transaction["merchant_lat"],
            "merchant_long": transaction["merchant_long"],
            "merchant_category": transaction["merchant_category"],
            "transaction_type": transaction["transaction_type"]
        })
    
    def get_velocity_6h(self, cc_num, current_time):
        """Count transactions in last 6 hours"""
        six_hours_ago = current_time - timedelta(hours=6)
        count = 0
        for txn in self.transactions[cc_num]:
            txn_time = datetime.strptime(txn["timestamp"], "%Y-%m-%d %H:%M:%S")
            if txn_time >= six_hours_ago:
                count += 1
        return count
    
    def get_avg_spend_30d(self, cc_num, current_time):
        """Calculate average spending in last 30 days"""
        thirty_days_ago = current_time - timedelta(days=30)
        amounts = []
        for txn in self.transactions[cc_num]:
            txn_time = datetime.strptime(txn["timestamp"], "%Y-%m-%d %H:%M:%S")
            if txn_time >= thirty_days_ago:
                amounts.append(txn["amount"])
        if amounts:
            return sum(amounts) / len(amounts)
        return 0
    
    def get_last_transaction(self, cc_num):
        """Get the most recent transaction for distance_speed calculation"""
        if self.transactions[cc_num]:
            return self.transactions[cc_num][-1]
        return None
