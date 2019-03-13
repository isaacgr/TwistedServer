from client.client import HttpClient
from client.network_speed import GetSpeed
from twisted.internet import reactor, threads
from twisted.web.client import readBody


def post_speed(result):
    h = HttpClient()
    d = h.post('http://192.168.2.21:3000/api/data', body=result)

    def _cb_post(response):
        d = readBody(response)
        d.addCallback(_cb_body)

    def _eb_post(error):
        print error
        reactor.stop()

    def _cb_body(body):
        print 'Got response\n'
        print body
        reactor.stop()

    d.addCallback(_cb_post)
    d.addErrback(_eb_post)

def main():
   g = GetSpeed()
   h = HttpClient()
   d = threads.deferToThread(g.get_speed)
   d.addCallback(post_speed)


if __name__=='__main__':
    main()
    reactor.run()
