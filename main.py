from client.web_client import WebClient
from client.network_speed import GetSpeed
from client.internet_addr import InterAddr
from twisted.internet import reactor, threads, defer, task
from twisted.web.client import readBody
import json
import argparse
import logging

FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
datefmt = "%Y-%m-%d-%H:%M:%S"
logging.basicConfig(filename='webserver.log', level=logging.INFO,
                    format=FORMAT, datefmt=datefmt)


def parse_commandline():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--host',
        default='http://192.168.2.21',
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

    return parser.parse_args()


def main():
    options = parse_commandline()

    host = options.host
    port = options.port
    path = options.path

    server = WebClient(host, port, path)
    network = GetSpeed()
    int_addr = InterAddr()

    d1 = threads.deferToThread(network.get_speed)
    d2 = threads.deferToThread(int_addr.get_addr)
    d1.addCallback(server.post_data)
    d2.addCallback(server.post_data)
    d1.addErrback(server.failure)
    d2.addErrback(server.failure)

    t = task.LoopingCall(main)
    t.start(1200)


if __name__ == '__main__':
    main()
    reactor.run()
