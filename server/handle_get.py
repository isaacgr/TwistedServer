from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
import json
import cgi

class Get(Resource):
    isLeaf = True

    def render_GET(self, request):
        uri = request.uri
        args = request.args
        path = request.path
        r = {"uri": uri, "path":path, "args": args}
        return json.dumps(r)

factory = Site(Get())
reactor.listenTCP(8080, factory)
reactor.run()
