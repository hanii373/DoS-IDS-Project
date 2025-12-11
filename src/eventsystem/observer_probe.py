from eventsystem.observer import Observer

class ProbeLogger(Observer):
    def on_event(self, data):
        print("🔍 PROBE DETECTED — scanning behavior:")
        print("   Features:", data["features"])
        print("   Probability:", data["prob"])
