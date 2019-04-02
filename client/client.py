from twisted.web.client import Agent
from twisted.internet import reactor
from twisted.web.http_headers import Headers
import json
from bytesprod import BytesProducer

agent = Agent(reactor)


class HttpClient(object):
    def __init__(self):
        pass

    def post(self, url, body={}, headers={}):
        if not headers:
            raise Exception('Missing headers')
        request = BytesProducer(json.dumps(body))
        d = agent.request(
            'POST',
            url,
            Headers(headers),
            request)
        return d
