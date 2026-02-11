from radar.interfaces.scanner import Scanner
import threading
import time
import random

class MockScanner(Scanner):
    def __init__(self, callback):
        super().__init__(callback)
        self._stop_event = threading.Event()

    def start(self):
        self.running = True
        print("[!] Running in MOCK_MODE. Generating fake data...")
        self.thread = threading.Thread(target=self._mock_loop, daemon=True)
        self.thread.start()

    def _mock_loop(self):
        while self.running:
            mock_mac = f"00:11:22:33:44:{random.randint(10, 99)}"
            mock_rssi = random.randint(-90, -30)
            
            data = {
                "mac": mock_mac,
                "rssi": mock_rssi
            }
            self.callback(data)
            
            time.sleep(1) # Simulate detection every second

    def stop(self):
        self.running = False
        print("[*] Stopping MockScanner...")
