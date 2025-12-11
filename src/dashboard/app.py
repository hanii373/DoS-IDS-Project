import sys
import os

# ------------------------------------------------------
# ENSURE Python can see the project root AND src/
# ------------------------------------------------------
APP_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(APP_DIR, ".."))
ROOT_DIR = os.path.abspath(os.path.join(APP_DIR, "..", ".."))

# Add /src folder
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Add project root folder
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Debug logs (optional)
print("Loaded Dashboard with paths:")
print("  APP_DIR:", APP_DIR)
print("  SRC_DIR:", SRC_DIR)
print("  ROOT_DIR:", ROOT_DIR)

# ------------------------------------------------------
# NOW IMPORT WORKS
# ------------------------------------------------------
from predictor import predict_single, feature_template
from eventsystem.events import event_manager
from eventsystem.logger import AttackLogger
from eventsystem.alerter import Alerter
from eventsystem.mitigator import Mitigator
from eventsystem.observer_probe import ProbeLogger
from eventsystem.observer_anomaly import AnomalyLogger
from eventsystem.observer_highrisk import HighRiskAlerter

import streamlit as st
import pandas as pd




LOG_FILE = "logs/alerts.log"

st.set_page_config(page_title="IDS Dashboard", layout="wide")

# Title
st.title("🚨 Intrusion Detection System Dashboard")
st.write("Real-time monitoring of DoS attacks using ML models.")

# --- Sidebar Controls ---
st.sidebar.header("Controls")

if st.sidebar.button("Start Simulation"):
    st.sidebar.success("Simulation started. Check terminal output.")
    os.system("start cmd /c python src/simulator.py")

auto_refresh = st.sidebar.checkbox("Auto Refresh", value=True)

# --- Real-time Detection Section ---
st.subheader("Real-Time Detection")

col1, col2 = st.columns(2)

with col1:
    st.metric("Last Prediction", "Waiting...")

with col2:
    st.metric("Probability", "Waiting...")

# --- Alert Log Display ---
st.subheader("Attack Alerts (Latest)")

def load_alerts():
    if not os.path.exists(LOG_FILE):
        return pd.DataFrame(columns=["timestamp", "message"])
    
    rows = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            if "]" in line:
                timestamp = line.split("]")[0].replace("[", "")
                message = line.split("]")[1].strip()
                rows.append({"timestamp": timestamp, "message": message})
    return pd.DataFrame(rows[-20:])   # show only last 20 entries

placeholder = st.empty()

# Auto-refresh logic
if auto_refresh:
    while True:
        df = load_alerts()
        placeholder.dataframe(df)

        import asyncio

        async def wait():
            await asyncio.sleep(2)

        asyncio.run(wait())


        st.rerun()
else:
    df = load_alerts()
    placeholder.dataframe(df)
