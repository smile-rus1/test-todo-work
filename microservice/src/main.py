from fastapi import FastAPI

from src.api.init_app import init_app
from src.core.config_reader import config
from src.core.logging import setup_logging


def start_app():
    setup_logging()
    app = init_app(FastAPI(), config)

    return app


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        app="src.main:start_app",
        host=config.api.host,
        port=config.api.port,
        reload=True,
        factory=True,
        log_level="info",
    )
