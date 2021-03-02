from os import path
from typing import Optional, Tuple

from pywebostv.connection import WebOSClient


class ConnectionCache:

    TEMP_FILE_PATH = path.join(
        path.dirname(path.realpath(__file__)),
        '..',
        '.last_connection',
    )

    @classmethod
    def write(cls, client: WebOSClient):
        with open(cls.TEMP_FILE_PATH, 'w') as cache:
            cache.write(client.host)

    @classmethod
    def read(cls) -> Optional[Tuple[str, bytes]]:
        try:
            with open(cls.TEMP_FILE_PATH, 'r') as cache:
                return cache.readline().rstrip('\n') or None
        except FileNotFoundError:
            return None
