import speedtest
from logger import Logger

class GetSpeed(object):

    def __init__(self):
        pass

    @Logger(message='Getting internet speed')
    def get_speed(self):
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
