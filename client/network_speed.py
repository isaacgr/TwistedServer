import speedtest

class GetSpeed():
    def get_speed(self):
        print 'Getting internet speed'
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
