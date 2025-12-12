from plyer import notification
from eventsystem.observer import Observer

class Alerter(Observer):

    def on_event(self, data):
        """Called when ANY attack event is fired."""
        prob = data.get("prob")
        attack_type = data.get("type", "Unknown")
        src = data.get("src_ip", "unknown")

        print("ALERTER TRIGGERED — DEBUG")

        notify_attack(probability=prob, attack_type=attack_type, src_ip=src)

        print("🔔 Alerter notification sent.")


def notify_attack(probability, attack_type="DoS", src_ip="unknown"):
    """
    Uses PLYER notification engine.
    Completely eliminates win10toast crashes.
    """

    title = f"🚨 ATTACK DETECTED — {attack_type.upper()}"
    message = f"Probability: {probability:.4f}\nSource IP: {src_ip}"

    try:
        notification.notify(
            title=title,
            message=message,
            timeout=5,          
            app_name="IDS System"
        )
    except Exception as e:
        print(f"⚠ Notification failed: {e}")
