import sys
import os

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from radar.config import Config
from radar.application.services import TargetService
from radar.api.app import create_app

def main():
    # 1. Choose Scanner Implementation Based on Config
    if Config.MOCK_MODE:
        from radar.infrastructure.mock_scanner import MockScanner
        scanner = MockScanner(callback=None) # callback set by service
    else:
        from radar.infrastructure.scapy_scanner import ScapyScanner
        scanner = ScapyScanner(interface=Config.INTERFACE, callback=None)

    # 2. Initialize Service with Scanner (Dependency Injection)
    target_service = TargetService(scanner=scanner)

    # 3. Start Scanning Background Process
    target_service.start_scanning()

    # 4. Initialize Flask App with Service
    app = create_app(target_service)

    # 5. Run Flask App
    try:
        # Note: app.run is blocking
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n[*] Shutting down...")
    finally:
        target_service.stop_scanning()

if __name__ == "__main__":
    main()
