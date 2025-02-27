import json

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse


async def common_validation_exception(_, exc: IntegrityError):
    return JSONResponse(status_code=400, content="An error occurred, please try again later")


async def validation_exception(_, err: ValidationError | RequestValidationError):
    return JSONResponse(status_code=400, content=json.loads(err.json()))


async def request_validation_exception_handler(_, err: RequestValidationError):
    return JSONResponse(status_code=400, content=err.errors())
