from collections import deque
from os import environ
from sys import argv

from pywebostv.connection import WebOSClient
from pywebostv.controls import WebOSControlBase

controls_subsystems = {
    e: subsystem
    for subsystem in WebOSControlBase.__subclasses__()
    for e in subsystem.COMMANDS
}

if __name__ == '__main__':
    client = WebOSClient(environ.get('WEBOS_TV_IP_ADDRESS'))
    client.connect()
    deque(client.register({'client_key': environ.get('WEBOS_TV_SECRET')}), maxlen=0)
    getattr(controls_subsystems[argv[1]](client), argv[1])(*argv[2:])
