import logging
import sys
import typing as t
from functools import lru_cache

from loguru import logger

from koifish.api.core.logging import InterceptHandler
from koifish.api.core.config import Settings


class AppSettings(Settings):
    @property
    def fastapi_kwargs(self) -> t.Dict[str, t.Any]:
        return {
            "debug": self.DEBUG,
            "docs_url": self.DOCS_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "title": self.TITLE,
            "version": self.VERSION,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.LOGGERS:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.LOGGING_LEVEL)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.LOGGING_LEVEL}])


@lru_cache
def get_app_settings() -> AppSettings:
    config = AppSettings()
    return config
