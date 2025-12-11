# events.py
# Central event dispatcher for Observer Pattern

class EventManager:
    def __init__(self):
        self.subscribers = {}   # event_name → list of callbacks

    def subscribe(self, event_name, callback):
        """Register an observer for an event."""
        if event_name not in self.subscribers:
            self.subscribers[event_name] = []
        self.subscribers[event_name].append(callback)

    def publish(self, event_name, data):
        """Notify all observers subscribed to an event."""
        if event_name in self.subscribers:
            for callback in self.subscribers[event_name]:
                callback(data)


# --- DEBUG PRINT TO CONFIRM FILE IS LOADED ---
print("DEBUG: events.py loaded — event_manager created.")

# Global instance used throughout the IDS system
event_manager = EventManager()
