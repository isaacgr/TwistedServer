from twisted.internet import defer, reactor
from subprocess import Popen, PIPE
import logging

log = logging.getLogger(__name__)


class InterAddr(object):

    def __init__(self):
        pass

    def get_addr(self):
        log.info('Getting IP Address')
        p = Popen(["curl", "https://ipinfo.io/ip"],
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, error = p.communicate()
        output = output.rstrip("\n")
        log.info('Got IP address: %s' % output)
        if not p.returncode:
            return {
                "type": "utility",
                "description": "network address",
                "data": {
                    "ip": output
                }
            }
        return [error, p.returncode]
