import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from logging import getLogger
from sys import stdout

from pywebostv.connection import WebOSClient
from wakeonlan import send_magic_packet

from lg_webos_cli.caller import call, controls, controls_subsystems
from lg_webos_cli.connection_cache import ConnectionCache
from lg_webos_cli.formatter import format_controls_help
from lg_webos_cli.store import CredStorage

logger = getLogger(__name__)


def main():
    parser = ArgumentParser(description='LG WebOS CLI wrapper', formatter_class=RawTextHelpFormatter)
    parser.add_argument('method', type=str, help=format_controls_help(controls_subsystems))
    parser.add_argument('method_args', metavar='arguments', nargs='*', help='Method arguments ([arg])')
    args = parser.parse_args(None if sys.argv[1:] else ['-h'])

    if args.method == 'power_on':
        # TODO figure out how to enumerate network interfaces and find broadcast ip addr (netifaces?)
        send_magic_packet(ConnectionCache.read_mac(), ip_address='192.168.15.255')
        sys.exit()

    addr = ConnectionCache.read_addr()
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
        parser.print_help()
        sys.exit()

    stdout.write(str(call(client, args.method, args.method_args)))
