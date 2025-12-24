
import random
import uuid
from datetime import datetime
from faker import Faker
from config import CARD_TYPES, CARD_ISSUERS, MERCHANT_CATEGORIES, TRANSACTION_TYPES

fake = Faker()

def generate_cardholder():
    """Generate a fake cardholder profile"""
    return {
        "cc_num": fake.credit_card_number(card_type="visa16"),
        "card_type": random.choice(CARD_TYPES),
        "card_issuer": random.choice(CARD_ISSUERS),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "gender": random.choice(["M", "F"]),
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=80).strftime("%Y-%m-%d"),
        "street": fake.street_address(),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "zip": fake.zipcode(),
        "user_lat": float(fake.latitude()),
        "user_long": float(fake.longitude())
    }

def generate_merchant():
    """Generate a fake merchant"""
    category = random.choice(MERCHANT_CATEGORIES)
    return {
        "merchant": fake.company(),
        "merchant_category": category,
        "merchant_lat": float(fake.latitude()),
        "merchant_long": float(fake.longitude()),
        "merchant_zip": fake.zipcode(),
        "terminal_id": f"TRM_{uuid.uuid4().hex[:8].upper()}"
    }
