from contextlib import asynccontextmanager

from src.infrastructure.redis_db.config_redis import RedisConfig

import redis.asyncio as aioredis


@asynccontextmanager
async def get_session_redis(redis_config: RedisConfig):
    redis_pool = aioredis.Redis(
        host=redis_config.host, port=redis_config.port, decode_responses=True
    )
    try:
        yield redis_pool
    finally:
        await redis_pool.close()
