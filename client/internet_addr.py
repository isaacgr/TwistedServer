from twisted.internet import defer, reactor
from subprocess import Popen, PIPE
from logger import Logger

class InterAddr(object):

    def __init__(self):
        pass

    @Logger(message='Getting IP Address')
    def get_addr(self):
        p = Popen(["curl", "https://ipinfo.io/ip"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, error = p.communicate()
        output = output.rstrip("\n")
        if not p.returncode:
            return {
                "type": "utility",
                "description": "network address",
                "data":{
                    "ip": output
                    }
                }
        return [error, p.returncode]

