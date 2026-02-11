from abc import ABC, abstractmethod
from typing import Callable, Any

class Scanner(ABC):
    def __init__(self, callback: Callable[[Any], None]):
        self.callback = callback
        self.running = False

    @abstractmethod
    def start(self):
        """Inicia o processo de escaneamento."""
        pass

    @abstractmethod
    def stop(self):
        """Para o processo de escaneamento."""
        pass
