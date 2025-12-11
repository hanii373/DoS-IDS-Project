from eventsystem.observer import Observer
from win10toast_click import ToastNotifier

toast = ToastNotifier()

class Alerter(Observer):
    def on_event(self, data):
        print("ALERTER TRIGGERED — DEBUG")

        prob = data.get("prob", None)
        message = f"Attack detected! Probability={prob:.4f}"

        toast.show_toast(
            "⚠️ IDS Attack Alert",
            message,
            duration=5,
            threaded=True
        )

        print("🔔 Alerter notification sent.")


def notify_attack(probability, model="IDS"):
    """Direct popup from predictor without observer dispatch."""
    toast.show_toast(
        f"⚠️ {model} Attack Alert",
        f"Probability={probability:.4f}",
        duration=5,
        threaded=True
    )
    print("🔔 Direct notify_attack popup sent.")
