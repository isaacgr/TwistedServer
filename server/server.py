from twisted.web.static import File
from twisted.internet.defer import succeed
from klein import run, route
from requests.auth import HTTPDigestAuth
import requests

base_url = "http://192.168.2.46/cgi-bin/ptz.cgi?action=start&channel=0&code=GotoPreset&arg1=0&arg2=%s&arg3=0&arg4=0"

# stupid digest auth requires requests, which is blocking
@route('/api/preset', methods=['POST'])
def set_camera(request):
    preset = request.args.get('preset', [1])[0]
    url = base_url % preset
    requests.post(url, auth=HTTPDigestAuth('username', 'password'))
    return succeed('OK')

run('192.168.2.48', 8080)
