import os
import subprocess
import time
import sys
from pathlib import Path

# FIX: Add src folder to Python path
sys.path.append(os.path.abspath("src"))

# Observer system imports
from eventsystem.events import event_manager
from eventsystem.logger import AttackLogger
from eventsystem.alerter import Alerter
from eventsystem.mitigator import Mitigator
from eventsystem.observer import Observer
from eventsystem.observer_probe import ProbeLogger
from eventsystem.observer_anomaly import AnomalyLogger
from eventsystem.observer_highrisk import HighRiskAlerter


# ============================================
#  PATH SETUP
# ============================================
ROOT = Path(__file__).parent
SRC_DIR = ROOT / "src"
DASHBOARD = SRC_DIR / "dashboard" / "app.py"
SIMULATOR = SRC_DIR / "simulator.py"
LOG_DIR = ROOT / "logs"

# ============================================
#  ENVIRONMENT CHECK
# ============================================
def check_environment():
    print("\n🔍 Checking environment...")

    required_files = [
        ROOT / "models" / "baseline_model.joblib",
        ROOT / "models" / "ids_model.pt",
        ROOT / "models" / "scaler.pkl",
    ]

    missing = [f for f in required_files if not f.exists()]
    if missing:
        print("❌ Missing model files:")
        for f in missing:
            print("   -", f.name)
        print("\nRun train_models.py first.")
        return False

    print("✔ Models found")

    if not LOG_DIR.exists():
        LOG_DIR.mkdir()
        print("✔ Created logs/ directory")

    print("✔ Environment OK!\n")
    return True


# ============================================
#  START DASHBOARD
# ============================================
def start_dashboard():
    print("🚀 Launching Streamlit Dashboard...")
    subprocess.Popen(f'streamlit run "{DASHBOARD}"', shell=True)


# ============================================
#  START SIMULATOR
# ============================================
def start_simulator():
    print("🛰️ Starting Simulator...")
    subprocess.Popen(f'python "{SIMULATOR}"', shell=True)


# ============================================
#  CLEAR LOGS
# ============================================
def clear_logs():
    alert_file = LOG_DIR / "alerts.log"
    if alert_file.exists():
        alert_file.unlink()
        print("🧹 Cleared alerts.log")
    else:
        print("ℹ No log file found.")


# ============================================
#  REGISTER OBSERVERS (OBSERVER PATTERN)
# ============================================
def register_observers():
    logger = AttackLogger()
    alerter = Alerter()
    mitigator = Mitigator()

    probe_logger = ProbeLogger()
    anomaly_logger = AnomalyLogger()
    highrisk_alerter = HighRiskAlerter()

    # DoS (Alerter, Logger, Mitigator)
    event_manager.subscribe("dos_attack_detected", logger.on_event)
    event_manager.subscribe("dos_attack_detected", alerter.on_event)
    event_manager.subscribe("dos_attack_detected", mitigator.on_event)

    # Probe
    event_manager.subscribe("probe_detected", probe_logger.on_event)
    event_manager.subscribe("probe_detected", alerter.on_event)   # <-- NEW

    # Anomaly
    event_manager.subscribe("anomaly_detected", anomaly_logger.on_event)
    event_manager.subscribe("anomaly_detected", alerter.on_event) # <-- NEW

    # High Risk
    event_manager.subscribe("high_risk_detected", highrisk_alerter.on_event)
    event_manager.subscribe("high_risk_detected", alerter.on_event) # <-- NEW

    print("🔔 All observers registered (DoS, Probe, Anomaly, High-Risk)")




# ============================================
#  MENU DISPLAY
# ============================================
def menu():
    print("""
===========================================
         IDS MAIN CONTROL PANEL
===========================================

1. Start Dashboard
2. Start Simulator
3. Start Both (Dashboard + Simulator)
4. Clear Alerts Log
5. Exit

===========================================
""")


# ============================================
#  MAIN FUNCTION
# ============================================
def main():
    if not check_environment():
        return

    # Register Observers BEFORE starting anything
    register_observers()

    while True:
        menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            start_dashboard()

        elif choice == "2":
            start_simulator()

        elif choice == "3":
            start_dashboard()
            time.sleep(2)
            start_simulator()

        elif choice == "4":
            clear_logs()

        elif choice == "5":
            print("Exiting IDS System...")
            break

        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
