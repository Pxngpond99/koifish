from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from loguru import logger
from pprint import pformat


async def http422_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    logger.warning(pformat({"detail": exc.errors()}))
    return JSONResponse(
        content={"detail": jsonable_encoder(exc.errors())},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
