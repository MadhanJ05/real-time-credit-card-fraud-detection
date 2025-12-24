
import random
import uuid
import time
from datetime import datetime
from generators import generate_cardholder, generate_merchant
from config import TRANSACTION_TYPES

def generate_transaction(cardholder, merchant):
    """Generate a single transaction"""
    now = datetime.now()
    transaction_type = random.choice(TRANSACTION_TYPES)
    
    transaction = {
        # Transaction identifiers
        "transaction_id": f"TXN_{uuid.uuid4().hex[:12].upper()}",
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "unix_time": int(time.time()),
        
        # Card info
        "cc_num": cardholder["cc_num"],
        "card_type": cardholder["card_type"],
        "card_issuer": cardholder["card_issuer"],
        
        # Cardholder profile
        "first_name": cardholder["first_name"],
        "last_name": cardholder["last_name"],
        "gender": cardholder["gender"],
        "dob": cardholder["dob"],
        
        # Cardholder address
        "street": cardholder["street"],
        "city": cardholder["city"],
        "state": cardholder["state"],
        "zip": cardholder["zip"],
        "user_lat": cardholder["user_lat"],
        "user_long": cardholder["user_long"],
        
        # Amount
        "amount": round(random.uniform(1.00, 500.00), 2),
        "currency": "USD",
        
        # Merchant info
        "merchant": merchant["merchant"],
        "merchant_category": merchant["merchant_category"],
        "merchant_lat": merchant["merchant_lat"],
        "merchant_long": merchant["merchant_long"],
        "merchant_zip": merchant["merchant_zip"],
        "terminal_id": merchant["terminal_id"] if transaction_type != "online" else None,
        
        # Transaction context
        "transaction_type": transaction_type,
        
        # Label
        "is_fraud": 0
    }
    
    return transaction
