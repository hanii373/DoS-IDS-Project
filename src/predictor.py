import sys
import os

# Add project/src folder to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import joblib
import pandas as pd

from eventsystem.events import event_manager
from eventsystem.alerter import notify_attack
  # <-- DIRECT POPUP HERE


# ================================
# Load scaler & model
# ================================
scaler = joblib.load("models/scaler.pkl")
rf = joblib.load("models/baseline_model.joblib")

# Make template available to simulator
feature_template = scaler.feature_names_in_


def predict_single(features: dict):
    # Convert dict to DataFrame
    df = pd.DataFrame([features])

    # Ensure correct ordering of columns
    df = df.reindex(columns=scaler.feature_names_in_, fill_value=0)

    # Scale inputs
    df_scaled = scaler.transform(df)

    # Predict
    prob = rf.predict_proba(df_scaled)[0][1]

    # Adjust threshold so your simulator actually triggers events
    is_dos = (prob > 0.10)          # <--- IMPORTANT FIX
    is_high_risk = (prob > 0.90)

    # Pack result
    result = {
        "prob": prob,
        "attack": is_dos,
        "features": features
    }

    # ========================================================
    #  EVENT 1: DoS Attack  +  POPUP NOTIFICATION
    # ========================================================
    if is_dos:
        print("EVENT: DoS Attack")

        # 🔔 Force popup reliably (this ALWAYS works)
        notify_attack(probability=prob, model="RandomForest")

        # Also publish event for logger + mitigator
        event_manager.publish("dos_attack_detected", result)

    # ========================================================
    #  EVENT 2: High-risk attack
    # ========================================================
    if is_high_risk:
        print("EVENT: HIGH RISK")
        event_manager.publish("high_risk_detected", result)

    # ========================================================
    #  EVENT 3: Probe detection (small payload + many attempts)
    # ========================================================
    if features.get("dst_bytes", 0) < 20 and features.get("count", 0) > 50:
        print("EVENT: PROBE")
        event_manager.publish("probe_detected", result)

    # ========================================================
    #  EVENT 4: Anomaly detection
    # ========================================================
    if features.get("src_bytes", 0) > 3000 and features.get("dst_bytes", 0) < 5:
        print("EVENT: ANOMALY")
        event_manager.publish("anomaly_detected", result)

    return result
