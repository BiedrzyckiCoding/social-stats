from abc import ABC, abstractmethod

class PlatformInterface(ABC):
    @abstractmethod
    def fetch_stats(self, username: str):
        pass
