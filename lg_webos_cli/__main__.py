from argparse import ArgumentParser
from logging import getLogger
from sys import argv, stdout, exit

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
        clients = {str(index): client for index, client
                   in enumerate(WebOSClient.discover(), 1)}
        entered = None
        while entered is None or entered not in clients.keys():
            entered = input('\n'.join([
                *[') '.join([i, c.host]) for i, c in clients.items()],
                '(q to quit)\n',
            ]))
            if entered == 'q':
                exit()
        client = clients.get(entered)
        addr = client.host
    else:
        client = WebOSClient(addr)
    client.connect()
    store = CredStorage.load(addr)
    for status in client.register(store):
        if status == WebOSClient.PROMPTED:
            print('Please accept the connection on the TV')
            ConnectionCache.write(client)
        if status == WebOSClient.REGISTERED:
            CredStorage.persist(addr, store)

    getattr(controls_subsystems[argv[1]](client), argv[1])(*argv[2:])
