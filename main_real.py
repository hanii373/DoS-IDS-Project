import json
import time
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
sys.path.append(SRC_DIR)

from predictor import predict_single, feature_template
from eventsystem.events import event_manager
from eventsystem.logger import AttackLogger
from eventsystem.alerter import Alerter
from eventsystem.mitigator import Mitigator
from eventsystem.observer_probe import ProbeLogger
from eventsystem.observer_anomaly import AnomalyLogger
from eventsystem.observer_highrisk import HighRiskAlerter

def register_observers():
    logger = AttackLogger()
    alerter = Alerter()
    mitigator = Mitigator()

    probe_logger = ProbeLogger()
    anomaly_logger = AnomalyLogger()
    highrisk_alerter = HighRiskAlerter()

    event_manager.subscribe("dos_attack_detected", logger.on_event)
    event_manager.subscribe("dos_attack_detected", alerter.on_event)
    event_manager.subscribe("dos_attack_detected", mitigator.on_event)

    event_manager.subscribe("probe_detected", probe_logger.on_event)
    event_manager.subscribe("anomaly_detected", anomaly_logger.on_event)
    event_manager.subscribe("high_risk_detected", highrisk_alerter.on_event)

    print("🔔 Observers registered for REAL traffic simulation.\n")

def load_packets(path):
    with open(path, "r") as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = [data]  

    packets = []
    for packet in data:
        full = {feature: 0 for feature in feature_template}
        for key, value in packet.items():
            if key in full:
                full[key] = value
        packets.append(full)

    return packets

def main():
    register_observers()

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("       REAL ATTACK SIMULATION MENU")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    print("1. Run DoS attack sample")
    print("2. Run Probe attack sample")
    print("3. Run Anomaly sample")
    print("4. Run Mixed Scenario")
    print("5. Exit\n")

    choice = input("Choose an option: ").strip()

    attack_map = {
        "1": "attacks/sample_dos.json",
        "2": "attacks/sample_probe.json",
        "3": "attacks/sample_anomaly.json",
        "4": "attacks/scenario_mixed.json",
    }

    if choice not in attack_map:
        print("Exiting.")
        return

    path = attack_map[choice]
    print(f"\n📁 Loading scenario: {path}\n")

    packets = load_packets(path)

    for i, pkt in enumerate(packets, start=1):
        print(f"\n➡ Processing packet {i}/{len(packets)}:")

        prob, attack_type = predict_single(pkt)

        print(f"Detected Type: {attack_type}")
        print(f"Probability: {prob:.4f}")

        time.sleep(1)

    print("\n✔ Real simulation complete.\n")

if __name__ == "__main__":
    main()
