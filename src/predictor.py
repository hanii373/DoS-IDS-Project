import joblib
import pandas as pd
from preprocess import preprocess_features
from eventsystem.events import event_manager
from eventsystem.alerter import notify_attack

scaler = joblib.load("models/scaler.pkl")
model = joblib.load("models/baseline_model.joblib")

feature_template = scaler.feature_names_in_


def predict_single(features):
    X = preprocess_features(features)

    prob = model.predict_proba(X)[0][1]

    if features["src_bytes"] > 4000 and features["count"] > 100:
        attack_type = "DoS"
        event_name = "dos_attack_detected"

    elif features["count"] > 60 and features["srv_count"] > 10:
        attack_type = "Probe"
        event_name = "probe_detected"

    elif prob > 0.15:
        attack_type = "Anomaly"
        event_name = "anomaly_detected"

    else:
        attack_type = "Normal"
        event_name = None

    result = {
        "prob": prob,
        "src_ip": features.get("src_ip", "unknown"),
        "attack": attack_type != "Normal",
        "type": attack_type,
        "features": features
    }

    if attack_type != "Normal":
        notify_attack(prob, attack_type, result["src_ip"])

    if event_name:
        event_manager.publish(event_name, result)

    return prob, attack_type
