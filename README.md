# Racoon

Racoon is a Python-based tool for detecting and tracking Wi-Fi and BLE devices using packet sniffing. It provides a real-time web interface to visualize detected devices, their signal strength (RSSI), and estimated distance.

## Features

- **Real-time Detection**: Captures Wi-Fi Probe Requests and Beacons to identify devices.
- **Distance Estimation**: Calculates approximate distance based on RSSI values using the Log-Distance Path Loss model.
- **Web Interface**: A cyber-themed HUD for visualizing targets in a radar view.
- **Mock Mode**: Simulates device detection for development and testing without needing specific hardware.

## Installation

### Prerequisites

- Python 3.8+
- [Npcap](https://npcap.com/) (Windows only) or `libpcap` (Linux) for packet capture support.

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/racoon.git
    cd racoon
    ```

2.  **Install dependencies:**
    ```bash
    pip install flask scapy requests
    ```

## Usage

### Running the Application

To start the application, run the `main.py` entry point:

```bash
python main.py
```

By default, the application runs in **Mock Mode** if the `RADAR_MOCK_MODE` environment variable is not set to `False`.

### Accessing the Interface

Open your web browser and navigate to:

```
http://localhost:5000
```

You will see the radar interface updating with detected targets.

### Configuration

Configuration is managed in `radar/config.py` and can be overridden via environment variables:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `RADAR_INTERFACE` | The network interface to sniff on (e.g., `wlan0`, `mon0`) | `wlan0` |
| `RADAR_MOCK_MODE` | Set to `True` for simulation, `False` for real sniffing | `True` |

### Running in Real Mode (Linux/Raspberry Pi)

To run on a Raspberry Pi or Linux machine with a monitor-mode capable Wi-Fi adapter:

1.  **Enable Monitor Mode** on your interface (e.g., using `airmon-ng`).
2.  **Set Environment Variables**:
    ```bash
    export RADAR_INTERFACE=wlan0mon
    export RADAR_MOCK_MODE=False
    sudo python main.py
    ```

## Troubleshooting

-   **"Scapy not available"**: Ensure you have installed `scapy` and `libpcap`/`Npcap`.
-   **Permission Denied**: Sniffing requires root/administrator privileges. run with `sudo` on Linux or as Administrator on Windows.
-   **TemplateNotFound**: If you see this error, ensure you are running `python main.py` from the root directory of the project.

## Development

The project structure is as follows:

```
c:/Projects/me/racoon/
├── main.py                 # Entry point
├── radar/                  # Application package
│   ├── config.py           # Configuration
│   ├── domain/             # Business entities
│   ├── interfaces/         # Abstract interfaces
│   ├── infrastructure/     # Concrete implementations
│   ├── application/        # Application services
│   ├── api/                # Flask API
│   └── templates/          # HTML templates
└── radar_legacy.py         # Original script (backup)
```

## License

MIT
