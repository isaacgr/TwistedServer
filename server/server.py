from twisted.web.static import File
from klein import Klein

app = Klein()

@app.route('/', branch=True)
def home(request):
    return File('./public')

@app.route('/about')
def pg_about(request):
    return 'The about page'

app.run('192.168.2.48', 8080)
