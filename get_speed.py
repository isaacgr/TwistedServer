import speedtest
from twisted.internet import defer, threads, reactor


class GetSpeed():
    def get_speed(self):
        s = speedtest.Speedtest()
        s.get_best_server()
        s.download()
        s.upload()
        res = s.results.dict()
        return [res["download"], res["upload"], res["ping"]]

    def print_data(self,result):
        print result
        reactor.stop()

    def start(self):
        d = threads.deferToThread(self.get_speed)
        d.addCallback(self.print_data)
        print 'Getting internet speed'


g = GetSpeed()
g.start()
reactor.run()
