import time
from typing import Dict, List, Any
from radar.domain.models import Target
from radar.interfaces.scanner import Scanner
from radar.config import Config

class TargetService:
    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.targets: Dict[str, Target] = {}
        # Set callback
        self.scanner.callback = self.process_detection

    def start_scanning(self):
        """Starts the scanner."""
        self.scanner.start()
        
    def stop_scanning(self):
        """Stops the scanner."""
        self.scanner.stop()

    def process_detection(self, data: Dict[str, Any]):
        """Callback to process raw detection data."""
        mac = data.get("mac")
        rssi = data.get("rssi")
        
        if mac and rssi is not None:
            distance = Target.update_signal(rssi)
            
            target = Target(
                mac=mac,
                rssi=rssi,
                distance=distance,
                last_seen=time.time()
            )
            self.targets[mac] = target

    def get_active_targets(self) -> List[Dict[str, Any]]:
        """
        Returns list of active targets, filtering out old ones.
        """
        active_targets = []
        keys_to_delete = []
        
        for mac, target in self.targets.items():
            if not target.is_active(Config.TARGET_TIMEOUT):
                keys_to_delete.append(mac)
            else:
                active_targets.append({
                    "mac": target.mac,
                    "rssi": target.rssi,
                    "distance": target.distance
                })

        
        # Cleanup
        for key in keys_to_delete:
            del self.targets[key]
            
        return active_targets
