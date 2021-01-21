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
            cache.writelines([
                client.host + '\n',
                client.key.decode(),
            ])

    @ classmethod
    def read(cls) -> Optional[Tuple[str, bytes]]:
        try:
            with open(cls.TEMP_FILE_PATH, 'r') as cache:
                addr, key = [x.rstrip('\n') for x in cache.readlines()]
                return (addr, key)
        except FileNotFoundError:
            return None
