import typing as t
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging
import os

APP_ENV: str = ""


class Settings(BaseSettings):
    # base
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    DEBUG: bool = False
    DOCS_URL: str = "/docs"
    OPENAPI_PREFIX: str = ""
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    REDIS_URL: str = "redis://localhost:6379"
    TITLE: str = "koifish"
    VERSION: str = "0.0.1"

    # database
    DB_ENGINE_MAPPER: dict = {
        "postgresql": "postgresql",
        "mysql": "mysql+pymysql",
        "mongodb": "mongodb",
    }
    DB: str = "mongodb"
    DB_HOST: str = "localhost"
    DB_PORT: int = 27017
    DB_USER: str = ""
    MONGODB_DB: str = ""
    DB_PASSWORD: str = ""
    DB_ENGINE: str = DB_ENGINE_MAPPER[DB]
    DATABASE_URI_FORMAT: str = (
        "{db_engine}://{user}:{password}@{host}:{port}/{database}"
    )
    DATABASE_URI: str = ""

    # auth
    SECRET_KEY: str = "Th1s_1s_my_3xampl3_0f_s3cr3t_k3y_0123456789"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 24 * 60  # 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60  # 7 days

    API_PREFIX: str = "/api"

    # CORS
    ALLOWED_HOSTS: t.List[str] = ["*"]

    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: t.Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    # find query
    PAGE: int = 1
    PAGE_SIZE: int = 20

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=(".env.test", ".env"),
    )



class TestConfigs(Settings):
    APP_ENV: str = "test"


settings = Settings()

if APP_ENV == "prod":
    pass
elif APP_ENV == "stage":
    pass
elif APP_ENV == "test":
    settings = TestConfigs()
