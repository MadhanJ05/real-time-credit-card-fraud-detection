
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pymongo import MongoClient

# Page config
st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="🚨",
    layout="wide"
)

# MongoDB connection
@st.cache_resource
def get_database():
    client = MongoClient("mongodb+srv://fraudadmin:JC3OCH5EY6J2OLWV@fraud-detection.ctfeedr.mongodb.net/?appName=fraud-detection")
    return client["fraud_detection"]

db = get_database()

# Title
st.title("🚨 Real-Time Credit Card Fraud Detection")
st.markdown("---")

# Metrics row
col1, col2, col3, col4 = st.columns(4)

total_txns = db.transactions.count_documents({})
fraud_alerts = db.fraud_alerts.count_documents({})
fraud_rate = (fraud_alerts / total_txns * 100) if total_txns > 0 else 0

with col1:
    st.metric("Total Transactions", f"{total_txns:,}")

with col2:
    st.metric("Fraud Alerts", f"{fraud_alerts:,}")

with col3:
    st.metric("Fraud Rate", f"{fraud_rate:.2f}%")

with col4:
    st.metric("Legitimate", f"{total_txns - fraud_alerts:,}")

st.markdown("---")

# Two columns for tables
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📋 Recent Transactions")
    recent_txns = list(db.transactions.find().sort("stored_at", -1).limit(10))
    if recent_txns:
        df_txns = pd.DataFrame(recent_txns)
        df_display = df_txns[["first_name", "last_name", "amount", "merchant_category", "predicted_fraud"]].copy()
        df_display.columns = ["First Name", "Last Name", "Amount", "Category", "Fraud"]
        df_display["Amount"] = df_display["Amount"].apply(lambda x: f"${x:.2f}")
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.write("No transactions yet")

with col_right:
    st.subheader("🚨 Recent Fraud Alerts")
    recent_fraud = list(db.fraud_alerts.find().sort("alerted_at", -1).limit(10))
    if recent_fraud:
        df_fraud = pd.DataFrame(recent_fraud)
        df_fraud_display = df_fraud[["first_name", "last_name", "amount", "fraud_reasons"]].copy()
        df_fraud_display.columns = ["First Name", "Last Name", "Amount", "Reasons"]
        df_fraud_display["Amount"] = df_fraud_display["Amount"].apply(lambda x: f"${x:.2f}")
        df_fraud_display["Reasons"] = df_fraud_display["Reasons"].apply(lambda x: ", ".join(x) if x else "")
        st.dataframe(df_fraud_display, use_container_width=True, hide_index=True)
    else:
        st.write("No fraud alerts yet")

st.markdown("---")

# Fraud by type
st.subheader("📊 Fraud Detection Breakdown")

fraud_with_reasons = list(db.fraud_alerts.find({"fraud_reasons": {"$exists": True}}))
if fraud_with_reasons:
    reason_counts = {}
    for txn in fraud_with_reasons:
        for reason in txn.get("fraud_reasons", []):
            if "velocity" in reason.lower():
                reason_counts["High Velocity"] = reason_counts.get("High Velocity", 0) + 1
            elif "travel" in reason.lower():
                reason_counts["Impossible Travel"] = reason_counts.get("Impossible Travel", 0) + 1
            elif "amount" in reason.lower():
                reason_counts["Amount Anomaly"] = reason_counts.get("Amount Anomaly", 0) + 1
            elif "hour" in reason.lower():
                reason_counts["Odd Hours"] = reason_counts.get("Odd Hours", 0) + 1
    
    if reason_counts:
        df_reasons = pd.DataFrame(list(reason_counts.items()), columns=["Fraud Type", "Count"])
        st.bar_chart(df_reasons.set_index("Fraud Type"))
else:
    st.write("No fraud data to display")

# Auto refresh
st.markdown("---")
if st.button("🔄 Refresh Data"):
    st.rerun()
