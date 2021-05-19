from os import path
from typing import Optional

from pywebostv.connection import WebOSClient
from getmac import get_mac_address


class ConnectionCache:

    KEY_IP_ADDR = 0
    KEY_MAC_ADDR = 1
    TEMP_FILE_PATH = path.join(
        path.dirname(path.realpath(__file__)),
        '..',
        '.last_connection',
    )

    @classmethod
    def write(cls, client: WebOSClient):
        with open(cls.TEMP_FILE_PATH, 'w') as cache:
            cache.write('\n'.join([
                client.host,
                get_mac_address(client.host),
            ]))

    @classmethod
    def read_addr(cls) -> Optional[str]:
        return cls._read(cls.KEY_IP_ADDR)

    @classmethod
    def read_mac(cls) -> Optional[str]:
        return cls._read(cls.KEY_MAC_ADDR)

    @classmethod
    def _read(cls, key: int) -> Optional[str]:
        try:
            with open(cls.TEMP_FILE_PATH, 'r') as cache:
                return cache.readlines()[key].rstrip('\n') or None
        except FileNotFoundError:
            return None
