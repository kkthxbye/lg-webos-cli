from typing import List, Optional

from pywebostv.connection import WebOSClient
from pywebostv.controls import WebOSControlBase
from wakeonlan import send_magic_packet

from lg_webos_cli.connection_cache import ConnectionCache


class WOLControl(WebOSControlBase):
    COMMANDS = {
        "power_on": {}
    }


controls_subsystems = {
    e: (subsystem, opts)
    for subsystem in WebOSControlBase.__subclasses__()
    for e, opts in subsystem.COMMANDS.items()
}

controls = controls_subsystems.keys()


def call(client: WebOSClient, method: str, args: Optional[List[str]]):
    subsystem = controls_subsystems[method][0](client)
    command = getattr(subsystem, method)
    return command(*args)
