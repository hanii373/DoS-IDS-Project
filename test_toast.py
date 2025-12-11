from win10toast import ToastNotifier
import time

toast = ToastNotifier()
toast.show_toast(
    "Test Notification",
    "If you see this, win10toast works 🙂",
    duration=5,
    threaded=False
)

# Give Windows time to show it before the script exits
time.sleep(6)
