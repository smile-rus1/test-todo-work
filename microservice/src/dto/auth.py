from dataclasses import dataclass


@dataclass
class UserDataAuth:
    username: str
    password: str


@dataclass
class Token:
    access_token: str
    refresh_token: str
