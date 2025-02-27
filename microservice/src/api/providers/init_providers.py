from fastapi import FastAPI

from src.core.config import Config
from src.api.providers import abstract
from src.api.providers import common, repo, services


def bind_common(app: FastAPI, config: Config):
    app.dependency_overrides[abstract.common.session_provider] = common.postgres_db_session(config)
    app.dependency_overrides[abstract.common.redis_provider] = common.redis_db_session(config)
    app.dependency_overrides[abstract.repo.comments_repo_provider] = repo.comments_repo_getter
    app.dependency_overrides[abstract.repo.redis_repo_provider] = repo.redis_repo_getter


def bind_services(app: FastAPI):
    app.dependency_overrides[abstract.services.comments_service_provider] = services.comments_service_getter
    app.dependency_overrides[abstract.services.auth_service_provider] = services.auth_service_getter


def bind_providers(app: FastAPI, config: Config):
    bind_common(app, config)
    bind_services(app)
