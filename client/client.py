from twisted.web.client import Agent
from twisted.internet import reactor
from twisted.web.http_headers import Headers
import json
from bytesprod import BytesProducer

agent = Agent(reactor)

class HttpClient(object):
    def __init__(self):
        self.headers = {'User-Agent': ['Twisted Client'],
                     'Content-Type': ['application/json']}

    def post(self, url, body={}, headers={}):
        if not headers:
            headers = self.headers
        request = BytesProducer(json.dumps(body))
        d = agent.request(
            'POST',
            url,
            Headers(headers),
            request)
        return d