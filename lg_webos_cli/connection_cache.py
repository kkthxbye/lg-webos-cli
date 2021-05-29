from json import dumps, loads
from os import path
from typing import Optional

from getmac import get_mac_address
from pywebostv.connection import WebOSClient


class ConnectionCache:

    KEY_IP_ADDR = 'ip_addr'
    KEY_MAC_ADDR = 'mac_addr'
    TEMP_FILE_PATH = path.join(
        path.dirname(path.realpath(__file__)),
        '..',
        '.last_connection',
    )

    @classmethod
    def write(cls, client: WebOSClient):
        with open(cls.TEMP_FILE_PATH, 'w') as cache:
            cache.write(dumps({
                cls.KEY_IP_ADDR: client.host,
                cls.KEY_MAC_ADDR: get_mac_address(client.host),
            }))

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
                return loads(cache.read()).get(key) or None
        except FileNotFoundError:
            return None
