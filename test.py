from client.client import HttpClient
from client.network_speed import GetSpeed
from twisted.internet import reactor, threads
from twisted.web.client import readBody


def post_speed(result):
    headers = {'User-Agent': ['Twisted Client'],
                     'Content-Type': ['application/json']}

    client = HttpClient()
    d = client.post('http://192.168.2.21:3000/api/data', body=result, headers=headers)

    d.addCallback(_cb_post)
    d.addErrback(_eb_post)

def _cb_post(response):
    d = readBody(response)
    d.addCallback(_cb_body)

def _eb_post(error):
    print 'POST Error: %s' % error
    reactor.stop()

def _cb_body(body):
    print 'Got response\n'
    print body
    reactor.stop()

def failure(error):
    print 'Error: %s' % error

def main():
   network = GetSpeed()
   d = threads.deferToThread(network.get_speed)
   d.addCallback(post_speed)
   d.addErrback(failure)

if __name__=='__main__':
    main()
    reactor.run()
