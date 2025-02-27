from fastapi import Depends

from src.api.providers.abstract.common import redis_provider
from src.api.providers.abstract.repo import comments_repo_provider, redis_repo_provider
from src.core.config_reader import config
from src.infrastructure.postgres.repo.comments_repo import CommentsRepo
from src.infrastructure.redis_db.redis_repo import RedisRepo
from src.services.auth.auth import AuthService
from src.services.comments.comments import CommentService


def comments_service_getter(
        comments_repo: CommentsRepo = Depends(comments_repo_provider),
        redis_repo: RedisRepo = Depends(redis_repo_provider)
):
    backend_api_url = config.api.backend_api_url
    return CommentService(
        comments_repo=comments_repo,
        redis_repo=redis_repo,
        backend_api_url=backend_api_url
    )


def auth_service_getter():
    auth_service = AuthService(backend_api_url=config.api.backend_api_url)
    return auth_service
