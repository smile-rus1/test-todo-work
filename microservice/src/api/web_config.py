from dataclasses import dataclass


@dataclass
class APIConfig:
    host: str
    port: int
    debug: bool
    backend_api_url: str
