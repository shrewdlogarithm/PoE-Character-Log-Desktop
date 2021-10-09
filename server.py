import os
from http import server
from bottle import Bottle, ServerAdapter, static_file,template, request
import process,utils

def start():
    global server
    class MyServer(ServerAdapter):
        server = None

        def run(self, handler):
            from wsgiref.simple_server import make_server, WSGIRequestHandler
            if self.quiet:
                class QuietHandler(WSGIRequestHandler):
                    def log_request(*args, **kw): pass
                self.options['handler_class'] = QuietHandler
            self.server = make_server(self.host, self.port, handler, **self.options)
            self.server.serve_forever()

        def stop(self):
            self.server.shutdown()

    app = Bottle()

    @app.route('/')
    def index():
        return template(utils.base_path +"templates/index.tpl",{"options": utils.options,"logs": utils.getlogs()})
    
    @app.route('/css/<filename>')
    def server_static(filename):
        return static_file(filename, root="./css")

    @app.route("/settings")
    def settings():
        return template(utils.base_path +"templates/settings.tpl",{"options": utils.options})

    @app.route("/savesettings", method='POST')
    def savesettings():
        message = "Settings Saved OK"
        if "clientlog" in request.POST:
            utils.setopt("clientlog",request.POST["clientlog"])
            if not os.path.exists(request.POST["clientlog"]):
                message = "Client Log not found"
        if "account" in request.POST:
            utils.setopt("account",request.POST["account"])
            api = process.getprofile()
            if api.status_code != 200:
                message = "Account not found or private"
        return template(utils.base_path +"templates/settings.tpl",{"message": message,"options": utils.options})
        
    server = MyServer(port=8080)
    try:
        app.run(server=server)
    except:
        print('server error')
    finally:
        print("server closed")        

def stop():
    global server
    server.stop()