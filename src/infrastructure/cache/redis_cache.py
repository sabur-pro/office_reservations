import json
from typing import Any, Optional

import redis

from config.logging import get_logger

from ...application.interfaces.cache import CacheInterface

logger = get_logger(__name__)


class RedisCache(CacheInterface):
    def __init__(self, redis_url: str) -> None:
        self._client: Optional[redis.Redis] = None  # type: ignore[type-arg]
        self._redis_url = redis_url
        self._connect()

    def _connect(self) -> None:
        try:
            self._client = redis.from_url(self._redis_url, decode_responses=True)
            self._client.ping()
            logger.info("Redis connection established")
        except redis.ConnectionError as e:
            logger.warning(f"Redis connection failed: {e}. Caching disabled.")
            self._client = None

    def get(self, key: str) -> Optional[Any]:
        if not self._client:
            return None

        try:
            value = self._client.get(key)
            if value:
                logger.debug(f"Cache HIT: {key}")
                return json.loads(value)
            logger.debug(f"Cache MISS: {key}")
            return None
        except (redis.RedisError, json.JSONDecodeError) as e:
            logger.error(f"Cache get error: {e}")
            return None

    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> bool:
        if not self._client:
            return False

        try:
            serialized = json.dumps(value, ensure_ascii=False, default=str)
            self._client.setex(key, ttl_seconds, serialized)
            logger.debug(f"Cache SET: {key} (TTL: {ttl_seconds}s)")
            return True
        except (redis.RedisError, TypeError) as e:
            logger.error(f"Cache set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        if not self._client:
            return False

        try:
            result = self._client.delete(key)
            logger.debug(f"Cache DELETE: {key}")
            return result > 0
        except redis.RedisError as e:
            logger.error(f"Cache delete error: {e}")
            return False

    def delete_pattern(self, pattern: str) -> int:
        if not self._client:
            return 0

        try:
            keys = self._client.keys(pattern)
            if keys:
                deleted = self._client.delete(*keys)
                logger.debug(f"Cache DELETE pattern '{pattern}': {deleted} keys")
                return deleted
            return 0
        except redis.RedisError as e:
            logger.error(f"Cache delete pattern error: {e}")
            return 0

    def increment(self, key: str, ttl_seconds: int = 60) -> int:
        if not self._client:
            return 0

        try:
            pipe = self._client.pipeline()
            pipe.incr(key)
            pipe.expire(key, ttl_seconds)
            result = pipe.execute()
            return result[0]
        except redis.RedisError as e:
            logger.error(f"Cache increment error: {e}")
            return 0
