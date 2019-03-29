from client.client import HttpClient
from client.network_speed import GetSpeed
from client.internet_addr import InterAddr
from twisted.internet import reactor, threads, defer, task
from twisted.web.client import readBody
import json
import logging

FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
datefmt = "%Y-%m-%d-%H:%M:%S"
logging.basicConfig(filename='/var/log/webserver.log', level=logging.INFO,\
    format=FORMAT, datefmt=datefmt)
log = logging.getLogger(__name__)

URL = 'http://192.168.2.21'
PORT = None
PATH = '/api/data'


class WebServer(object):

    def __init__(self, url=URL, port=PORT, path=PATH):
        self.url = url + ':'+ str(port) + path
        self.headers = {'User-Agent': ['Twisted Client'],
                         'Content-Type': ['application/json']}

    def post_data(self, result):
        client = HttpClient()
        d = client.post(self.url, body=result, headers=self.headers)
        d.addCallback(self._cb_post)
        d.addErrback(self._eb_post)
        return d

    def _cb_post(self, response):
        log.info('Post successful')
        d = readBody(response)
        d.addCallback(self._cb_body)
        return d

    def _eb_post(self, error):
        log.info('POST Error: %s' % error)
        # reactor.stop()

    def _cb_body(self, body):
        log.info('Response: %s' % json.loads(body))
        return defer.succeed(body)

    def failure(self, error):
        log.info('Error: %s' % error)
        # reactor.stop()

def main():
    server = WebServer(port=3000)
    network = GetSpeed()
    int_addr = InterAddr()
    d1 = threads.deferToThread(network.get_speed)
    d2 = threads.deferToThread(int_addr.get_addr)
    d1.addCallback(server.post_data)
    d2.addCallback(server.post_data)
    # d.addCallback(lambda _: reactor.stop())
    d1.addErrback(server.failure)
    d2.addErrback(server.failure)

if __name__=='__main__':
    t = task.LoopingCall(main)
    t.start(1200)
    reactor.run()
