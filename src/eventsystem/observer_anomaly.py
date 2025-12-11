from eventsystem.observer import Observer

class AnomalyLogger(Observer):
    def on_event(self, data):
        print("⚠️ ANOMALY DETECTED — unusual traffic pattern:")
        print("   Features:", data["features"])
        print("   Probability:", data["prob"])
