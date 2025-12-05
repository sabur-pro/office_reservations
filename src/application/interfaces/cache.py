from abc import ABC, abstractmethod
from typing import Any, Optional


class CacheInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> bool:
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        pass

    @abstractmethod
    def delete_pattern(self, pattern: str) -> int:
        pass

    @abstractmethod
    def increment(self, key: str, ttl_seconds: int = 60) -> int:
        pass
