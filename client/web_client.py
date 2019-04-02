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
        d.addCallback(self.parse_response, 'POST')
        d.addErrback(self.failure)
        return d

    def parse_response(self, response, method='POST'):
        log.info('{} successful'.format(method))
        d = readBody(response)
        d.addCallback(self._cb_parse_response)
        return d

    def _cb_parse_response(self, body):
        log.info('Response: %s' % json.loads(body))
        return defer.succeed(body)

    def failure(self, error):
        log.info('Error: %s' % error)
        return defer.fail(error)
