
import random
import uuid
import time
import math
from datetime import datetime, timedelta
from generators import generate_merchant
from config import TRANSACTION_TYPES, MERCHANT_CATEGORIES

def calculate_distance(lat1, long1, lat2, long2):
    """Calculate distance between two points in km"""
    R = 6371  # Earth's radius in km
    lat1, long1, lat2, long2 = map(math.radians, [lat1, long1, lat2, long2])
    dlat = lat2 - lat1
    dlong = long2 - long1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlong/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def generate_fraud_transaction(cardholder, history_tracker, fraud_type=None):
    """Generate a fraudulent transaction"""
    
    # Get last transaction to check if impossible_travel is valid
    last_txn = history_tracker.get_last_transaction(cardholder["cc_num"])
    
    # Available fraud types
    available_fraud_types = ["velocity_attack", "amount_anomaly", "odd_hours", "category_mismatch"]
    
    # Only add impossible_travel if last transaction was physical (not online)
    if last_txn and last_txn.get("transaction_type") != "online":
        available_fraud_types.append("impossible_travel")
    
    if fraud_type is None:
        fraud_type = random.choice(available_fraud_types)
    elif fraud_type == "impossible_travel" and (not last_txn or last_txn.get("transaction_type") == "online"):
        # Requested impossible_travel but not valid, pick another
        fraud_type = random.choice(["velocity_attack", "amount_anomaly", "odd_hours", "category_mismatch"])
    
    now = datetime.now()
    merchant = generate_merchant()
    
    # For impossible_travel, force physical transaction
    if fraud_type == "impossible_travel":
        transaction_type = random.choice(["in_store", "contactless", "chip", "swipe"])
    else:
        transaction_type = random.choice(TRANSACTION_TYPES)
    
    # Base transaction
    transaction = {
        "transaction_id": f"TXN_{uuid.uuid4().hex[:12].upper()}",
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "unix_time": int(time.time()),
        "cc_num": cardholder["cc_num"],
        "card_type": cardholder["card_type"],
        "card_issuer": cardholder["card_issuer"],
        "first_name": cardholder["first_name"],
        "last_name": cardholder["last_name"],
        "gender": cardholder["gender"],
        "dob": cardholder["dob"],
        "street": cardholder["street"],
        "city": cardholder["city"],
        "state": cardholder["state"],
        "zip": cardholder["zip"],
        "user_lat": cardholder["user_lat"],
        "user_long": cardholder["user_long"],
        "amount": round(random.uniform(1.00, 500.00), 2),
        "currency": "USD",
        "merchant": merchant["merchant"],
        "merchant_category": merchant["merchant_category"],
        "merchant_lat": merchant["merchant_lat"],
        "merchant_long": merchant["merchant_long"],
        "merchant_zip": merchant["merchant_zip"],
        "terminal_id": merchant["terminal_id"] if transaction_type != "online" else None,
        "transaction_type": transaction_type,
        "is_fraud": 1,
        "fraud_type": fraud_type
    }
    
    # Apply fraud pattern
    if fraud_type == "impossible_travel":
        # Transaction far from last physical transaction location
        if last_txn:
            # Place merchant on opposite side of world
            transaction["merchant_lat"] = -last_txn["merchant_lat"]
            transaction["merchant_long"] = -last_txn["merchant_long"]
    
    elif fraud_type == "velocity_attack":
        # Multiple rapid transactions - amount stays same, just flag it
        pass  # The velocity will be detected by velocity_6h feature
    
    elif fraud_type == "amount_anomaly":
        # Unusually high amount
        avg_spend = history_tracker.get_avg_spend_30d(cardholder["cc_num"], now)
        if avg_spend > 0:
            transaction["amount"] = round(avg_spend * random.uniform(10, 20), 2)
        else:
            transaction["amount"] = round(random.uniform(2000, 10000), 2)
    
    elif fraud_type == "odd_hours":
        # Transaction at suspicious hour (2-5 AM)
        odd_hour = random.randint(2, 5)
        odd_time = now.replace(hour=odd_hour, minute=random.randint(0, 59))
        transaction["timestamp"] = odd_time.strftime("%Y-%m-%d %H:%M:%S")
    
    elif fraud_type == "category_mismatch":
        # Unusual category for this user - pick high-risk category
        high_risk = ["jewelry", "electronics", "money_transfer", "gaming"]
        transaction["merchant_category"] = random.choice(high_risk)
    
    return transaction
