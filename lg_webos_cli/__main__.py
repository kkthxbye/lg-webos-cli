import sys
from argparse import ArgumentParser
from logging import getLogger
from sys import stdout

from pywebostv.connection import WebOSClient
from pywebostv.controls import WebOSControlBase

from lg_webos_cli.caller import call, controls
from lg_webos_cli.connection_cache import ConnectionCache
from lg_webos_cli.store import CredStorage

logger = getLogger(__name__)

controls_subsystems = {
    e: subsystem
    for subsystem in WebOSControlBase.__subclasses__()
    for e in subsystem.COMMANDS
}

if __name__ == '__main__':
    parser = ArgumentParser(description='LG WebOS CLI wrapper')
    parser.add_argument('method', type=str, help=', '.join(controls))
    parser.add_argument('method_args', metavar='arguments', nargs='*', help='Optional arguments')
    args = parser.parse_args()

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
                sys.exit()
        client = clients.get(entered)
    else:
        client = WebOSClient(addr)
    client.connect()
    store = CredStorage.load(client.host)
    for status in client.register(store):
        if status == WebOSClient.PROMPTED:
            print('Please accept the connection on the TV')
            ConnectionCache.write(client)
        if status == WebOSClient.REGISTERED:
            CredStorage.persist(client.host, store)
    if args.method not in controls:
        stdout.write(
            f'No method called "{args.method}".\n'
            f'Available methods: {", ".join(controls)}'
        )
        sys.exit()

    stdout.write(str(call(client, args.method, args.method_args)))
