
# 🚨 Real-Time Credit Card Fraud Detection

A real-time fraud detection system built from a **credit card company's perspective**, using streaming data pipelines and machine learning to identify fraudulent transactions.

## 🎯 Live Demo
**Dashboard:** [https://real-time-credit-card-fraud-detection-aa.streamlit.app](https://real-time-credit-card-fraud-detection-aa.streamlit.app)

---

## 📊 Architecture
```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Data Generation │────▶│  Apache Kafka    │────▶│ Stream Processing│
│                  │     │  (Confluent)     │     │                  │
│ • Cardholders    │     │                  │     │ • Feature Eng.   │
│ • Transactions   │     │ • transactions   │     │ • Fraud Detection│
│ • Fraud Patterns │     │ • fraud-alerts   │     │                  │
└──────────────────┘     └──────────────────┘     └────────┬─────────┘
                                                           │
                         ┌──────────────────┐              │
                         │    Streamlit     │◀─────────────┤
                         │    Dashboard     │              │
                         │                  │              ▼
                         │ • Real-time      │     ┌──────────────────┐
                         │   Metrics        │     │    MongoDB       │
                         │ • Fraud Alerts   │◀────│    Atlas         │
                         │ • Analytics      │     │                  │
                         └──────────────────┘     │ • Transactions   │
                                                  │ • Fraud Alerts   │
                                                  └──────────────────┘
```

---

## 🔍 Fraud Detection Patterns

| Pattern | Description | Detection Method |
|---------|-------------|------------------|
| **Impossible Travel** | Transaction location far from previous transaction in short time | `distance_speed > 1000 km/h` |
| **Velocity Attack** | Too many transactions in a short period | `velocity_6h > 5 transactions` |
| **Amount Anomaly** | Spending much higher than user's average | `avg_spend_diff > $500` |
| **Odd Hours** | Transactions at unusual times | `2 AM - 5 AM` |
| **Category Mismatch** | Sudden spending in high-risk categories | `jewelry, electronics, money_transfer` |

---

## 📈 Aggregated Features

| Feature | Description |
|---------|-------------|
| `velocity_6h` | Number of transactions in last 6 hours |
| `avg_spend_diff` | Difference between current amount and 30-day average |
| `distance_speed` | Speed required to travel between consecutive transactions (km/h) |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Streaming** | Apache Kafka (Confluent Cloud) |
| **Processing** | Python, PySpark |
| **Database** | MongoDB Atlas |
| **Cache** | Redis (Upstash) |
| **Dashboard** | Streamlit Cloud |
| **Environment** | Google Colab |

---

## 📁 Project Structure
```
real-time-credit-card-fraud-detection/
├── src/
│   ├── config.py                 # Constants and configurations
│   ├── generators.py             # Cardholder & merchant generators
│   ├── transaction_generator.py  # Transaction generator
│   ├── fraud_generator.py        # Fraud pattern generator
│   ├── history_tracker.py        # Transaction history tracking
│   ├── kafka_producer.py         # Kafka producer
│   ├── kafka_consumer.py         # Kafka consumer
│   ├── feature_engineering.py    # Aggregated feature calculation
│   ├── mongodb_storage.py        # MongoDB operations
│   └── fraud_pipeline.py         # Main fraud detection pipeline
├── streamlit_app.py              # Dashboard application
├── requirements.txt              # Python dependencies
└── README.md
```

---

## 📊 Data Schema (22 Fields)

**Transaction Identifiers:**
- `transaction_id`, `timestamp`, `unix_time`

**Card Information:**
- `cc_num`, `card_type`, `card_issuer`

**Cardholder Profile:**
- `first_name`, `last_name`, `gender`, `dob`

**Cardholder Address:**
- `street`, `city`, `state`, `zip`, `user_lat`, `user_long`

**Transaction Details:**
- `amount`, `currency`

**Merchant Information:**
- `merchant`, `merchant_category`, `merchant_lat`, `merchant_long`, `merchant_zip`, `terminal_id`

**Context:**
- `transaction_type` (in_store, online, contactless, chip, swipe)

**Label:**
- `is_fraud` (0 = legitimate, 1 = fraud)

---

## 🚀 How It Works

1. **Data Generation**: Synthetic transactions are generated with realistic patterns
2. **Streaming**: Transactions flow through Kafka topics in real-time
3. **Feature Engineering**: Aggregated features (velocity, spending patterns, travel speed) are calculated
4. **Fraud Detection**: Rule-based detection flags suspicious transactions
5. **Storage**: All transactions stored in MongoDB, fraud alerts stored separately
6. **Visualization**: Real-time dashboard shows metrics and alerts

---

## 🏃 Running the Project

### Prerequisites
- Confluent Cloud account (Kafka)
- MongoDB Atlas account
- Streamlit Cloud account
- Google Colab (for processing)

### Quick Start
1. Clone the repository
2. Set up your Kafka, MongoDB, and Redis credentials
3. Run the fraud pipeline in Google Colab
4. View the dashboard at the Streamlit URL

---

## 📧 Contact

**Author:** Madhan J
**GitHub:** [@MadhanJ05](https://github.com/MadhanJ05)

---

## 📄 License

This project is for educational and portfolio purposes.
