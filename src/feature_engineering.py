
import math
from datetime import datetime
from history_tracker import TransactionHistory

class FeatureEngineer:
    def __init__(self):
        self.history = TransactionHistory()
    
    def calculate_distance(self, lat1, long1, lat2, long2):
        """Calculate distance between two points in km"""
        R = 6371
        lat1, long1, lat2, long2 = map(math.radians, [lat1, long1, lat2, long2])
        dlat = lat2 - lat1
        dlong = long2 - long1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlong/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c
    
    def add_features(self, transaction):
        """Add aggregated features to a transaction"""
        cc_num = transaction["cc_num"]
        current_time = datetime.strptime(transaction["timestamp"], "%Y-%m-%d %H:%M:%S")
        
        # Velocity: transactions in last 6 hours
        velocity_6h = self.history.get_velocity_6h(cc_num, current_time)
        
        # Average spend difference
        avg_spend = self.history.get_avg_spend_30d(cc_num, current_time)
        if avg_spend > 0:
            avg_spend_diff = transaction["amount"] - avg_spend
        else:
            avg_spend_diff = 0
        
        # Distance speed (impossible travel detection)
        last_txn = self.history.get_last_transaction(cc_num)
        if last_txn and last_txn.get("transaction_type") != "online" and transaction["transaction_type"] != "online":
            distance = self.calculate_distance(
                last_txn["merchant_lat"], last_txn["merchant_long"],
                transaction["merchant_lat"], transaction["merchant_long"]
            )
            last_time = datetime.strptime(last_txn["timestamp"], "%Y-%m-%d %H:%M:%S")
            time_diff_hours = (current_time - last_time).total_seconds() / 3600
            if time_diff_hours > 0:
                distance_speed = distance / time_diff_hours  # km per hour
            else:
                distance_speed = 0
        else:
            distance_speed = 0
        
        # Add features to transaction
        transaction["velocity_6h"] = velocity_6h
        transaction["avg_spend_diff"] = round(avg_spend_diff, 2)
        transaction["distance_speed"] = round(distance_speed, 2)
        
        # Add to history for future calculations
        self.history.add_transaction(cc_num, transaction)
        
        return transaction
