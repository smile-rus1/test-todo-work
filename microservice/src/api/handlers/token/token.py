from fastapi import APIRouter, status, Depends, Response

from src.api.handlers.token.request import AuthData
from src.api.providers.abstract.services import auth_service_provider
from src.dto.auth import Token, UserDataAuth
from src.services.auth.auth import AuthService


token_api = APIRouter(prefix="/token", tags=["Auth"])


@token_api.post(
    "",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=Token
)
async def authenticate_user(
        response: Response,
        auth_data: AuthData,
        auth_service: AuthService = Depends(auth_service_provider)
):
    dto = UserDataAuth(**auth_data.model_dump())
    token = await auth_service.authenticate_user(dto)

    response.set_cookie(key="access_token", value=token.access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=token.refresh_token, httponly=True)

    return Token(**token.__dict__)
