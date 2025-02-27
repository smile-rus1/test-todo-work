import os

from dotenv import load_dotenv

from src.core.config import Config
from src.api.web_config import APIConfig
from src.infrastructure.postgres.db_config import DBConfig
from src.infrastructure.redis_db.config_redis import RedisConfig


def config_loader() -> Config:
    load_dotenv()

    return Config(
        api=APIConfig(
            host=os.getenv("WEB_HOST"),
            port=int(os.getenv("WEB_PORT")),
            debug=bool(os.getenv("DEBUG")),
            backend_api_url=os.getenv("BACKEND_API_URL")
        ),
        db=DBConfig(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            db_name=os.getenv("DB_NAME"),
            driver=os.getenv("DB_DRIVER")
        ),
        redis=RedisConfig(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT"))
        )
    )


config = config_loader()
