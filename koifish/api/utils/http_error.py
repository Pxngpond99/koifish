from fastapi import HTTPException
from fastapi.utils import is_body_allowed_for_status_code
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response
from loguru import logger


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    logger.warning({"detail": exc.detail})
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code, headers=headers)
