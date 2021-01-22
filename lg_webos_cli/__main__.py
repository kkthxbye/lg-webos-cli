from argparse import ArgumentParser
from collections import deque
from logging import getLogger
from os import environ
from sys import argv, stdout

from pywebostv.connection import WebOSClient
from pywebostv.controls import WebOSControlBase

from lg_webos_cli.connection_cache import ConnectionCache
from lg_webos_cli.store import CredStorage

logger = getLogger(__name__)

controls_subsystems = {
    e: subsystem
    for subsystem in WebOSControlBase.__subclasses__()
    for e in subsystem.COMMANDS
}

# parser = ArgumentParser(description='#TODO')
# parser.add_argument('method', metavar='method', type=str, help='#TODO')
# args = parser.parse_args()

if __name__ == '__main__':
    addr = ConnectionCache.read()
    if not addr:
        clients = WebOSClient.discover()
        print(clients)

    client = WebOSClient(addr)
    client.connect()
    store = CredStorage.load(addr)
    for status in client.register(store):
        if status == WebOSClient.PROMPTED:
            print('Please accept the connection on the TV!')
            ConnectionCache.write(client)
        if status == WebOSClient.REGISTERED:
            CredStorage.persist(addr, store)

    getattr(controls_subsystems[argv[1]](client), argv[1])(*argv[2:])
