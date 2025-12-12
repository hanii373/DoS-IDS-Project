import warnings
warnings.filterwarnings(
    "ignore",
    message="X has feature names, but RandomForestClassifier was fitted without feature names"
)

from scapy.all import sniff, IP, TCP, UDP
from predictor import predict_single, feature_template
import time

def extract_features(packet):
    features = {f: 0 for f in feature_template}

    if IP in packet:
        features["src_bytes"] = len(packet)
        features["dst_bytes"] = 0
        features["count"] = 1
        features["srv_count"] = 1

        if TCP in packet:
            features["protocol_type_tcp"] = 1
        elif UDP in packet:
            features["protocol_type_udp"] = 1

    return features

def handle_packet(packet):
    features = extract_features(packet)

    prob, attack_type = predict_single(features)

    print(f"[Sniffer] prob={prob:.4f} | type={attack_type}")

def start_sniffer(duration=10):
    """
    Start packet sniffer for a LIMITED time (seconds)
    """
    print(f"🛰️ Live packet sniffer started for {duration} seconds...")
    try:
        sniff(
            prn=handle_packet,
            store=False,
            timeout=duration
        )
    except KeyboardInterrupt:
        print("🛑 Sniffer manually stopped.")

    print("✅ Sniffer finished.\n")
