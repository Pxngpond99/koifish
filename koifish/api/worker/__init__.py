from .server import WorkerServer
from koifish.api.core.app import get_app_settings, AppSettings


def create_server():

    settings = get_app_settings()
    server = WorkerServer(settings)

    return server
