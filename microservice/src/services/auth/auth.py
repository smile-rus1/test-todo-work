from abc import ABC

import aiohttp

from src.dto.auth import UserDataAuth, Token


class AuthUseCase(ABC):
    def __init__(self, backend_api_url: str):
        self._backend_api_url = backend_api_url


class AuthenticateUser(AuthUseCase):
    async def __call__(self, auth_data: UserDataAuth) -> Token:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    f"{self._backend_api_url}/api/accounts/token/",
                    json=auth_data.__dict__
            ) as response:
                result = await response.json()
                return Token(access_token=result.get("access"), refresh_token=result.get("refresh"))


class AuthService:
    def __init__(self, backend_api_url: str):
        self._backend_api_url = backend_api_url

    async def authenticate_user(self, auth_data: UserDataAuth) -> Token:
        return await AuthenticateUser(self._backend_api_url)(auth_data)
