
# Card types
CARD_TYPES = ["Visa", "Mastercard", "Amex", "Discover"]

# Card issuers (US banks - major and regional)
CARD_ISSUERS = [
    # Big 4
    "Chase", "Bank of America", "Wells Fargo", "Citi",
    # Major national
    "Capital One", "US Bank", "PNC", "Truist", "TD Bank",
    "Fifth Third", "Regions", "KeyBank", "Huntington", "M&T Bank",
    # Credit card focused
    "American Express", "Discover Bank", "Barclays", "Synchrony",
    # Online/digital
    "Goldman Sachs", "Ally Bank", "Marcus", "SoFi",
    # Credit unions
    "Navy Federal", "USAA", "Pentagon Federal", "State Employees CU",
    # Retail cards
    "Comenity Bank", "Bread Financial"
]

# Merchant categories (based on real MCC codes)
MERCHANT_CATEGORIES = [
    # Daily essentials
    "grocery", "gas_station", "pharmacy", "convenience_store",
    # Food & drink
    "restaurant", "fast_food", "coffee_shop", "bar_nightclub", "food_delivery",
    # Shopping
    "clothing", "department_store", "online_shopping", "electronics", 
    "furniture", "home_improvement", "sporting_goods", "jewelry",
    # Services
    "healthcare", "utilities", "subscription_services", "gym_fitness", 
    "salon_spa", "auto_repair",
    # Travel & transport
    "airline", "hotel", "car_rental", "rideshare", "parking",
    # Entertainment
    "movies", "streaming_services", "gaming",
    # Financial
    "atm_withdrawal", "money_transfer"
]

# Transaction types
TRANSACTION_TYPES = ["in_store", "online", "contactless"]
