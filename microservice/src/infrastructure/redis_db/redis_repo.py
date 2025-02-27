import json
from typing import Any

from redis.asyncio import Redis

from src.interfaces.repo import IRepo


class RedisRepo(IRepo):
    def __init__(self, redis_pool: Redis):
        self._redis_pool = redis_pool

    async def set_in_redis(self, key: str, comments: Any):
        value = json.dumps(comments)
        await self._redis_pool.setex(key, value=value, time=60)

    async def get_by_key(self, key: str) -> Any:
        values = await self._redis_pool.get(key)
        if values is None:
            return None
        return json.loads(values)
