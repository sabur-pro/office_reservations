from config.logging import get_logger

from ...application.interfaces.cache import CacheInterface

logger = get_logger(__name__)


class RateLimiter:
    def __init__(
        self,
        cache: CacheInterface,
        max_requests: int = 100,
        window_seconds: int = 60,
    ) -> None:
        self._cache = cache
        self._max_requests = max_requests
        self._window_seconds = window_seconds

    def is_allowed(self, client_ip: str) -> bool:
        key = f"rate_limit:{client_ip}"
        count = self._cache.increment(key, self._window_seconds)

        if count == 0:
            return True

        if count > self._max_requests:
            logger.warning(f"Rate limit exceeded for IP: {client_ip} ({count} requests)")
            return False

        return True

    def get_remaining(self, client_ip: str) -> int:
        key = f"rate_limit:{client_ip}"
        cached = self._cache.get(key)

        if cached is None:
            return self._max_requests

        try:
            count = int(cached)
            return max(0, self._max_requests - count)
        except (ValueError, TypeError):
            return self._max_requests
