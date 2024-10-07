from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination.api import _add_pagination
from koifish.api.routers import init_router
from koifish.api.core.app import get_app_settings, AppSettings
from koifish.models import init_mongoengine
from koifish.api.utils.http_error import http_error_handler
from koifish.api.utils.validation_error import http422_error_handler
from koifish.api.redis_rq import init_rq, redis_queue
from koifish.api.worker import create_server


def create_app() -> FastAPI:
    settings: AppSettings = get_app_settings()
    settings.configure_logging()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # on app start up
        await init_router(app, settings)
        await init_mongoengine(settings)
        _add_pagination(app)
        yield
        # on app shutdown
        # await disconnect_mongoengine()

    app = FastAPI(**settings.fastapi_kwargs)
    init_rq(settings)
    app.router.lifespan_context = lifespan
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        return {"message": "service is working"}

    return app


# app = create_app
