import asyncio
import datetime
import json
import pathlib


import os

import redis
from rq import Worker, Queue, Connection, SimpleWorker
from koifish.api.core.app import get_app_settings, AppSettings
from koifish.models import init_mongoengine
import logging

logger = logging.getLogger(__name__)

listen = ["default"]


class koifishWorker(SimpleWorker):
    def __init__(self, *args, **kwargs):

        settings = kwargs.pop("settings")
        super().__init__(*args, **kwargs)

        async def init_mongo():
            await init_mongoengine(settings)

        asyncio.run(init_mongo())


class WorkerServer:
    def __init__(self, settings):
        self.settings = settings

        redis_url = settings.REDIS_URL
        self.conn = redis.from_url(redis_url)

        # logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.DEBUG)

    def run(self):
        with Connection(self.conn):
            worker = koifishWorker(list(map(Queue, listen)), settings=self.settings)
            worker.work()
