from typing import Dict
from json import loads, dumps

from keyring import get_password, set_password


class CredStorage:

    SERVICE_NAME = 'lg_webos_cli'

    @classmethod
    def persist(cls, addr: str, data: Dict[str, str]):
        set_password(cls.SERVICE_NAME, addr, dumps(data))

    @classmethod
    def load(cls, addr: str) -> Dict[str, str]:
        data = get_password(cls.SERVICE_NAME, addr)
        return loads(data) if data else {}
