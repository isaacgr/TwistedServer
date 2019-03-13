from twisted.internet import reactor, threads
from twisted.web.client import Agent, readBody
from twisted.web.http_headers import Headers
import json
from bytesprod import BytesProducer
from get_network_speed import GetSpeed

agent = Agent(reactor)

def post_data(result):
    print 'Got result %s' % result
    body = BytesProducer(json.dumps(result))
    d = agent.request(
        'POST',
        'http://httpbin.org/post',
        Headers({'User-Agent': ['Twisted Web Client Example'],
                 'Content-Type': ['application/json']}),
        body)

    def cbResponse(response):
        print 'Response received'
        d = readBody(response)
        d.addCallback(_cb_body)
    d.addCallback(cbResponse)

    def cbShutdown(ignored):
        print ignored
        reactor.stop()
    d.addBoth(cbShutdown)

    def _cb_body(body):
        print body

g = GetSpeed()
d = threads.deferToThread(g.get_speed)
d.addCallback(post_data)

reactor.run()
