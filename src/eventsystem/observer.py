# observer.py
# Base class for all observers

class Observer:
    def on_event(self, data):
        """
        All observers must override this method.
        Called automatically when an event is fired.
        """
        raise NotImplementedError("Observer must implement on_event()")
