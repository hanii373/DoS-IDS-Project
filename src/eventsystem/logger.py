# logger.py
# Logs attack events to logs/alerts.log

from datetime import datetime
from eventsystem.observer import Observer
from pathlib import Path


class AttackLogger(Observer):
    def __init__(self):
        # Ensure logs directory exists
        Path("logs").mkdir(exist_ok=True)

    def on_event(self, data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        prob = data.get("prob", None)
        src = data.get("features", {}).get("src_ip", "unknown")

        log_message = f"[{timestamp}] ATTACK DETECTED | prob={prob:.4f} | src={src}"

        with open("logs/alerts.log", "a") as f:
            f.write(log_message + "\n")

        print("📄 Logged attack:", log_message)
