from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import Config
from src.infrastructure.postgres.connections import get_postgres_connection
from src.infrastructure.redis_db.connections import get_session_redis


def postgres_db_session(config: Config):
    sessionmaker = get_postgres_connection(config.db)

    async def get_db_session() -> AsyncSession:
        async with sessionmaker() as session:
            yield session

    return get_db_session


def redis_db_session(config: Config):
    async def get_redis_session():
        async with get_session_redis(config.redis) as redis_pool:
            return redis_pool
    return get_redis_session
