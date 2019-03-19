from client.client import HttpClient
from client.network_speed import GetSpeed
from client.internet_addr import InterAddr
from twisted.internet import reactor, threads, defer
from twisted.web.client import readBody


def post_data(result):
    headers = {'User-Agent': ['Twisted Client'],
                     'Content-Type': ['application/json']}

    client = HttpClient()
    d = defer.Deferred()

    for value in result:
        d = client.post('http://192.168.2.21:3000/api/data', body=value, headers=headers)
        d.addCallback(_cb_post)
        d.addErrback(_eb_post)

    return d

def _cb_post(response):
    d = readBody(response)
    d.addCallback(_cb_body)
    return d

def _eb_post(error):
    print 'POST Error: %s' % error
    reactor.stop()

def _cb_body(body):
    print body
    return defer.succeed(body)

def failure(error):
    print 'Error: %s' % error
    reactor.stop()

def main():
   dl = []
   network = GetSpeed()
   int_addr = InterAddr()
   d1 = threads.deferToThread(network.get_speed)
   d2 = threads.deferToThread(int_addr.get_addr)
   dl.append(d1)
   dl.append(d2)
   d = defer.gatherResults(dl)
   d.addCallback(post_data)
   d.addCallback(lambda _: reactor.stop())
   d.addErrback(failure)

if __name__=='__main__':
    main()
    reactor.run()
