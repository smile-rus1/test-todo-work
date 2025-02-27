from dataclasses import dataclass

from src.api.web_config import APIConfig
from src.infrastructure.postgres.db_config import DBConfig
from src.infrastructure.redis_db.config_redis import RedisConfig


@dataclass
class Config:
    api: APIConfig
    db: DBConfig
    redis: RedisConfig
