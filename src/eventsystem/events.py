class EventManager:
    def __init__(self):
        self.subscribers = {} 

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

print("DEBUG: events.py loaded — event_manager created.")
event_manager = EventManager()
