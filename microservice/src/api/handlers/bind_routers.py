from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from src.api.handlers.comments.main import comments_router
from src.api.handlers.exceptions import validation_exception, request_validation_exception_handler, \
    common_validation_exception
from src.api.handlers.token.token import token_api


def bind_exceptions_handlers(app: FastAPI):
    app.add_exception_handler(ValidationError, validation_exception)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(IntegrityError, common_validation_exception)


def bind_routers(app: FastAPI):
    app.include_router(token_api)
    app.include_router(comments_router)
