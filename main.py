import sys
import os
import time
import subprocess

# FIX PYTHON PATHS SO ALL MODULES LOAD CORRECTLY
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# IMPORT PROJECT MODULES
from simulator import run_simulator_parallel
from sniffer import start_sniffer
from eventsystem.events import event_manager
from eventsystem.logger import AttackLogger
from eventsystem.alerter import Alerter
from eventsystem.mitigator import Mitigator
from eventsystem.observer_probe import ProbeLogger
from eventsystem.observer_anomaly import AnomalyLogger
from eventsystem.observer_highrisk import HighRiskAlerter
from predictor import scaler 

def register_observers():
    logger = AttackLogger()
    alerter = Alerter()
    mitigator = Mitigator()

    probe_logger = ProbeLogger()
    anomaly_logger = AnomalyLogger()
    highrisk = HighRiskAlerter()

    event_manager.subscribe("dos_attack_detected", logger.on_event)
    event_manager.subscribe("dos_attack_detected", alerter.on_event)
    event_manager.subscribe("dos_attack_detected", mitigator.on_event)

    event_manager.subscribe("probe_detected", probe_logger.on_event)
    event_manager.subscribe("anomaly_detected", anomaly_logger.on_event)
    event_manager.subscribe("high_risk_detected", highrisk.on_event)

    print("\n🔔 Observers registered.\n")

def start_dashboard():
    print("▶ Launching dashboard (Streamlit)...")
    subprocess.Popen(
        ["streamlit", "run", "src/dashboard/app.py"],
        shell=True
    )
    print("✔ Dashboard started at http://localhost:8501\n")

def main():
    print("Scaler loaded for runtime preprocessing.")
    register_observers()

    while True:
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("           IDS MAIN CONTROL PANEL")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        print("1. Run Parallel Simulator (3 seconds)")
        print("2. Run Dashboard")
        print("3. Run Simulator + Dashboard")
        print("4. Start Real Network Sniffer")
        print("5. Exit\n")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            print("\n🚀 Starting parallel simulator for 3 seconds...\n")
            run_simulator_parallel(duration=5)

        elif choice == "2":
            start_dashboard()

        elif choice == "3":
            start_dashboard()
            time.sleep(2)
            run_simulator_parallel(duration=3)

        elif choice == "4":
            print("🛰️ Live packet sniffer started… Press CTRL+C to stop.")
            try:
                start_sniffer(duration=10)
            except KeyboardInterrupt:
                print("\n🛑 Sniffer stopped.\n")

        elif choice == "5":
            print("Exiting IDS system. Goodbye!")
            break

        else:
            print("❌ Invalid choice, try again.")

if __name__ == "__main__":
    main()
