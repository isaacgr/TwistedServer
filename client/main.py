from web_client import WebClient
from network_speed import GetSpeed
from internet_addr import InterAddr
from twisted.internet import reactor, threads, defer, reactor
from twisted.web.client import readBody
import json
import argparse
import logging
import sys

FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
datefmt = "%Y-%m-%d-%H:%M:%S"
log = logging.getLogger(__name__)


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
        default=None,
        metavar='PORT',
        help='Port of server to connect to [%(default)s]'
    )

    parser.add_argument(
        '--path',
        default='/api/data',
        metavar='PATH',
        help='Path for the server, if any [%(default)s]'
    )

    parser.add_argument(
        '--log',
        default='/var/log/webserver.log',
        metavar='FILENAME',
        help='Logfile of client, if any [%(default)s]'
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

    log.info('Starting poll loop')
    loop(scheme, host, port, path)


def loop(scheme, host, port, path):

    try:
        server = WebClient(scheme, host, port, path)
        network = GetSpeed()
        int_addr = InterAddr()

        d1 = threads.deferToThread(network.get_speed)
        d2 = threads.deferToThread(int_addr.get_addr)
        d1.addCallback(server.post_data)
        d2.addCallback(server.post_data)
        d1.addErrback(server.failure)
        d2.addErrback(server.failure)
    except Exception:
        log.critical('Uncaught exception: ', exc_info=sys.exc_info())

    reactor.callLater(1200, loop, scheme, host, port, path)


if __name__ == '__main__':
    main()
    reactor.run()
