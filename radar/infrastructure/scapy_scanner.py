try:
    from scapy.all import sniff, Dot11ProbeReq, Dot11Beacon
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

from radar.interfaces.scanner import Scanner
import threading

class ScapyScanner(Scanner):
    def __init__(self, interface: str, callback):
        super().__init__(callback)
        self.interface = interface
        self._stop_event = threading.Event()

    def start(self):
        if not SCAPY_AVAILABLE:
            print("Scapy not available. Cannot start ScapyScanner.")
            return

        self.running = True
        print(f"[*] Starting packet capture on interface {self.interface} (Scapy)...")
        # Scapy's sniff blocks, so we run it in a thread if we want non-blocking start, 
        # or we rely on the caller to manage threads. 
        # Here, `sniff` calls the callback for each packet.
        # However, `sniff` is blocking by default. To make `start` non-blocking relative to the caller
        # if the caller expects it, we might wrap this. 
        # But `sniff` has `prn` callback. 
        # Let's assume start() spawns a thread to run sniff, as the original code did.
        
        self.thread = threading.Thread(target=self._sniff_loop, daemon=True)
        self.thread.start()

    def _sniff_loop(self):
        # Note: Scapy's sniff doesn't have a clean "stop" mechanism from outside nicely 
        # without stop_filter or similar, but for this simple refactor we will keep it simple.
        # store=False avoids keeping packets in memory.
        try:
             sniff(iface=self.interface, prn=self._packet_handler, store=False, 
                   stop_filter=lambda x: not self.running)
        except Exception as e:
            print(f"Error in Scapy sniffing: {e}")

    def _packet_handler(self, pkt):
        if not self.running:
            return
            
        if pkt.haslayer(Dot11ProbeReq) or pkt.haslayer(Dot11Beacon):
            # Extract basic info and pass to callback
            try:
                rssi = pkt.dBm_AntSignal
            except AttributeError:
                rssi = -90
            
            mac = pkt.addr2
            if mac:
                # We pass a dict or object to the callback. 
                # The callback in Application layer will convert to Domain object.
                data = {
                    "mac": mac,
                    "rssi": rssi
                }
                self.callback(data)

    def stop(self):
        self.running = False
        print("[*] Stopping ScapyScanner...")
