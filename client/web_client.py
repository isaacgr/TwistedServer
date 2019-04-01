from client import HttpClient
from twisted.internet import defer
from twisted.web.client import readBody
import json
import logging


log = logging.getLogger(__name__)


class WebClient(object):

    def __init__(self, scheme, url, port, path):
        self.url = scheme + url + ':' + str(port) + path
        self.headers = {'User-Agent': ['Twisted Client'],
                        'Content-Type': ['application/json']}

    def post_data(self, result):
        client = HttpClient()
        log.info('POST request: %s' % result)
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

    def _cb_body(self, body):
        log.info('Response: %s' % json.loads(body))
        return defer.succeed(body)

    def failure(self, error):
        log.info('Error: %s' % error)
        return defer.fail(error)
