from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.providers.abstract.common import session_provider, redis_provider
from src.infrastructure.postgres.repo.comments_repo import CommentsRepo
from src.infrastructure.redis_db.redis_repo import RedisRepo


def comments_repo_getter(
        session: AsyncSession = Depends(session_provider),
):
    return CommentsRepo(session=session)


def redis_repo_getter(
        session_redis: Redis = Depends(redis_provider)
):
    return RedisRepo(redis_pool=session_redis)
