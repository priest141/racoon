from dataclasses import dataclass
import time

@dataclass
class Target:
    mac: str
    rssi: int
    distance: float
    last_seen: float
    source: str

    _smoothed_rssi:int

    @staticmethod
    def update_signal(self, rssi:int):
        self.last_seen = time.time()
        
        alpha = 2.0
        if self._smoothed_rssi == None:
            self._smoothed_rssi = rssi
        else:
            self._smoothed_rssi = alpha * rssi + (1 - alpha) * self._smoothed_rssi

    self.calculate_distance(self._smoothed_rssi, self.source)

    @staticmethod
    def calculate_distance(rssi: int, tx_power: int, n: float, source: str) -> float:
        """
        Calcula a distância aproximada baseada no RSSI.
        """
        if self.source == "BLE":
            self.tx_power = -59.0
            self.n = 3.0
        else:
            self.tx_power = -45.0
            self.n = 2.5

        if self.rssi == 0:
            return -1.0 # Unknown or invalid
            
        ratio = (self.tx_power - self._smoothed_rssi) / (10 * n)
        distance = 10 ** ratio
        return round(distance, 2)

    def is_active(self, timeout_seconds: int) -> bool:
        """
        Verifica se o alvo foi visto recentemente dentro do timeout.
        """
        return (time.time() - self.last_seen) <= timeout_seconds

    def to_dict(self):
        """ Retorna o formato esperado pela API Flask """
        return {
            "mac": self.mac,
            "vendor": self.vendor,
            "source": self.source,
            "distance": self.distance,
            "rssi_raw": round(self._smoothed_rssi, 1)
        }
