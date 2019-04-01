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
        download = "%.2f Mbps" % (float(res['download'])/1000000)
        upload = "%.2f Mbps" % (float(res['upload'])/1000000)
        log.info('Got speed:[%s DOWN, %s UP]' % (download, upload))
        return {
            "type": "info",
            "description": "network speed",
            "data": {
                'download': download,
                'upload': upload
            }
        }
