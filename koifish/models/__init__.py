import pathlib
from mongoengine import connect, disconnect_all, DEFAULT_CONNECTION_NAME, Document
from flask_mongoengine import MongoEngine
from mongoengine.base.common import _get_documents_by_db
import mongoengine as me

import importlib
import logging

logger = logging.getLogger(__name__)

db = MongoEngine()


def regist_models(directory):
    for module in directory.iterdir():
        model_file = module / "models.py"

        if not model_file.exists():
            continue

        package = module.parts[len(pathlib.Path.cwd().parts) :]
        try:
            pymod_file = f"{'.'.join(package)}.{model_file.stem}"
            pymod = importlib.import_module(pymod_file)
            print("regit model:", pymod)
        except Exception as e:
            logger.exception(e)


def init_db(app):
    module_directory = pathlib.Path(__file__).parent.parent / "modules"
    regist_models(module_directory)

    # from . import oauth2

    db.init_app(app)

cls_documents: list[Document] = _get_documents_by_db(DEFAULT_CONNECTION_NAME, DEFAULT_CONNECTION_NAME)



async def init_mongoengine(settings):
    host = (
        settings.DATABASE_URI_FORMAT
        if settings.DB_USER and settings.DB_PASSWORD
        else "{db_engine}://{host}:{port}/{database}"
    ).format(
        db_engine=settings.DB_ENGINE,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.MONGODB_DB,
    )
    logger.info("DB URI: " + host)
    get_connection = connect(host=host)
    logger.info("Initialized mongengine")

    return get_connection
