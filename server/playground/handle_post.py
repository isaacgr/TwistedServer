from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
import cgi

class Post(Resource):
    isLeaf = True

    def render_POST(self, request):
        return 'OK'

factory = Site(Post())
reactor.listenTCP(8080, factory)
reactor.run()
