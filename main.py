from client.web_client import WebClient
from client.network_speed import GetSpeed
from client.internet_addr import InterAddr
from twisted.internet import reactor, threads, defer
from twisted.web.client import readBody
import json
import argparse
import logging

FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
datefmt = "%Y-%m-%d-%H:%M:%S"


def parse_commandline():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--scheme',
        default='http://',
        metavar='SCHEME',
        help='Scheme URL to connect to [%(default)s]'
    )

    parser.add_argument(
        '--host',
        default='192.168.2.21',
        metavar='HOST',
        help='Host URL to connect to [%(default)s]'
    )

    parser.add_argument(
        '--port',
        default=3000,
        metavar='PORT',
        help='Port of server to connect to [%(default)s]'
    )

    parser.add_argument(
        '--path',
        default='/api/data',
        metavar='PATH',
        help='Path of server, if any [%(default)s]'
    )

    parser.add_argument(
        '--log',
        default='/var/log/webserver.log',
        metavar='FILENAME',
        help='Path of server, if any [%(default)s]'
    )

    return parser.parse_args()


def main():
    options = parse_commandline()

    scheme = options.scheme
    host = options.host
    port = options.port
    path = options.path
    logfile = options.log

    logging.basicConfig(filename=logfile, level=logging.INFO,
                        format=FORMAT, datefmt=datefmt)

    server = WebClient(scheme, host, port, path)
    network = GetSpeed()
    int_addr = InterAddr()

    d1 = threads.deferToThread(network.get_speed)
    d2 = threads.deferToThread(int_addr.get_addr)
    d1.addCallback(server.post_data)
    d2.addCallback(server.post_data)
    d1.addErrback(server.failure)
    d2.addErrback(server.failure)


if __name__ == '__main__':
    main()
    reactor.run()
