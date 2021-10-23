import os,re
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
        return template(utils.base_path +"templates/index.tpl")
    
    @app.route('/css/<filename>')
    def server_static(filename):
        return static_file(filename, root=utils.base_path + "css")

    @app.route('/data/<filename>')
    def server_static(filename):
        return static_file(filename, root='./data')

    @app.route('/logs/<filename>')
    def server_static(filename):
        return static_file(filename, root='./logs')

    @app.route('/pob/builds/<filename>')
    def server_static(filename):
        return static_file(filename, root='./pob/builds')

    @app.route("/log")
    def log():
        return template(utils.base_path +"templates/log.tpl")

    @app.route('/logdata', method="POST")
    def logupdate():
        logdata = []
        lastlog = 0
        if "lastlog" in request.forms.dict:
            lastlog = parsedate(request.forms.get("lastlog"))
        try:
            f = open("poeclog.log", encoding='utf-8', errors='ignore')
            for li in f.readlines():
                if parsedate(li) > lastlog:
                    logdata.append(li)
        except:
            pass
        finally:
            f.close()
        return {"loglines": logdata}

    @app.route("/settings")
    def settings():
        return template(utils.base_path +"templates/settings.tpl")

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
                message = "Account not found or private?"
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

def parsedate(datestr):
    vals = re.search(r"^([0-9]+)/([0-9]+)/([0-9]+), ([0-9]+):([0-9]+):([0-9]+)",datestr)
    if vals:
        return int(vals.groups()[2].zfill(4) + vals.groups()[1].zfill(2) + vals.groups()[0].zfill(2) + vals.groups()[3].zfill(2) + vals.groups()[4].zfill(2) + vals.groups()[5].zfill(2))
    else:
        return 0