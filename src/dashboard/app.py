import sys
import os
import time
import streamlit as st
import pandas as pd

APP_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(APP_DIR, ".."))
ROOT_DIR = os.path.abspath(os.path.join(APP_DIR, "..", ".."))

for p in (SRC_DIR, ROOT_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

LOG_FILE = "logs/alerts.log"

st.set_page_config(
    page_title="IDS Dashboard",
    layout="wide",
    page_icon="🚨"
)

st.title("🚨 Intrusion Detection System Dashboard")
st.caption("Real-time monitoring of network attacks using ML + Observer Pattern")

st.sidebar.header("Controls")

auto_refresh = st.sidebar.checkbox("Auto Refresh", value=True)
refresh_interval = st.sidebar.slider(
    "Refresh interval (seconds)",
    min_value=1,
    max_value=10,
    value=2
)

def load_alerts():
    if not os.path.exists(LOG_FILE):
        return pd.DataFrame(
            columns=["timestamp", "type", "prob", "src_ip"]
        )

    rows = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            if "]" not in line:
                continue

            try:
                ts = line.split("]")[0].replace("[", "").strip()
                rest = line.split("]")[1].strip()

                parts = [p.strip() for p in rest.split("|")]

                attack_type = parts[0].replace("type=", "")
                prob = float(parts[1].replace("prob=", ""))
                src_ip = parts[2].replace("src=", "")

                rows.append({
                    "timestamp": ts,
                    "type": attack_type,
                    "prob": prob,
                    "src_ip": src_ip
                })
            except Exception:
                continue

    return pd.DataFrame(rows[-20:]) 

st.subheader("📊 Latest Detection")

df = load_alerts()

col1, col2, col3 = st.columns(3)

if len(df) > 0:
    last = df.iloc[-1]
    col1.metric("Attack Type", last["type"])
    col2.metric("Probability", f"{last['prob']:.4f}")
    col3.metric("Source IP", last["src_ip"])
else:
    col1.metric("Attack Type", "Waiting...")
    col2.metric("Probability", "Waiting...")
    col3.metric("Source IP", "Waiting...")

st.subheader("🚨 Attack Alerts (Latest)")

if len(df) == 0:
    st.info("No alerts yet.")
else:
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()
