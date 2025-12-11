from eventsystem.observer import Observer
from win10toast import ToastNotifier

toast = ToastNotifier()

class HighRiskAlerter(Observer):
    def on_event(self, data):
        prob = data.get("prob", 0)

        message = f"CRITICAL ATTACK! Probability = {prob:.4f}"
        toast.show_toast(
            "🚨 HIGH RISK ATTACK DETECTED",
            message,
            duration=5,
            threaded=True
        )

        print("🚨 HIGH-RISK alert sent:", message)
