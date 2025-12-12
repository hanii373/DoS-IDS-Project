from eventsystem.observer import Observer
import subprocess

class Mitigator(Observer):
    def on_event(self, data):
        features = data.get("features", {})
        src_ip = features.get("src_ip", None)

        if not src_ip:
            print("⚠ Mitigator triggered but no src_ip found.")
            return

        print(f"🛡 Auto-Mitigation triggered: Blocking IP {src_ip}")

        command = (
            f'netsh advfirewall firewall add rule '
            f'name="Block_{src_ip}" dir=in action=block remoteip={src_ip}'
        )

        try:
            subprocess.call(command, shell=True)
            print(f"🛡 Successfully blocked {src_ip}")
        except Exception as e:
            print("❌ Failed to block IP:", e)
