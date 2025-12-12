from datetime import datetime
from eventsystem.observer import Observer

class AttackLogger(Observer):

    def on_event(self, data):
        """
        Log attack metadata including attack type.
        """
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        prob = data.get("prob", 0)
        attack_type = data.get("type", "Unknown")
        src = data.get("src_ip", "unknown")

        line = (
            f"[{ts}] type={attack_type} | "
            f"prob={prob:.4f} | "
            f"src={src}\n"
        )

        with open("logs/alerts.log", "a") as f:
            f.write(line)

        print(f"📄 Logged attack: {line.strip()}")
