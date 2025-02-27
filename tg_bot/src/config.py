from dataclasses import dataclass
import os
from dotenv import load_dotenv


@dataclass
class Config:
    token: str
    backend_url: str
    microservice_url: str


def config_reader():
    load_dotenv()

    return Config(
        token=os.getenv("TOKEN_BOT"),
        backend_url=os.getenv("BACKEND_URL"),
        microservice_url=os.getenv("microservice_url")
    )


config = config_reader()
