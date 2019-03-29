import speedtest
import logging

log = logging.getLogger(__name__)

class GetSpeed(object):

    def __init__(self):
        pass

    def get_speed(self):
        log.info('Getting network speed')
        s = speedtest.Speedtest()
        s.get_best_server()
        s.download()
        s.upload()
        res = s.results.dict()
        return {
            "type": "info",
            "description": "network speed",
            "data": {
                'download': res["download"],
                'upload': res["upload"],
                'ping': res["ping"]
            }
        }
