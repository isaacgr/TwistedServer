from twisted.internet import defer, reactor
from subprocess import Popen, PIPE

class InterAddr(object):

    def __init__(self):
        pass

    def get_addr(self):
        print 'Getting internet ip'
        p = Popen(["curl", "https://ipinfo.io/ip"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, error = p.communicate()
        output = output.rstrip("\n")
        if not p.returncode:
            return {
                "type": "network address",
                "data":{
                    "ip": output
                    }
                }
        return [error, p.returncode]

