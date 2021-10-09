import os,time,threading,pystray,webbrowser
from PIL import Image
import server,process,utils

runprocess = True

# Process Thread
def doprocess(icon):
    global runprocess
    #process.loadprofile() # catch-up any characters/find the last active one
    while runprocess == True:        
        process.checklog()        
        time.sleep(5)
    print("process ending")

# Main Thread
def main(icon):   
    icon.visible = True

    pthread = threading.Thread(target=doprocess,args=[icon])
    pthread.start()

    server.start() # this is blocking

    print("main ending")

    pthread.join() # wait for process thread

    os._exit(0) # this ensures nothing gets left behind!

# Tray Setup 
def runupd(icon):
    global runprocess
    process.loadprofile()

def showpg(pg,icon):
    webbrowser.open("http://localhost:8080/" + pg)

def about(icon):
    webbrowser.open(utils.homep)

def exit_action(icon):
    global runprocess
    runprocess = False
    server.stop()

pystray.Icon('Icon', Image.open(utils.base_path + "poe.png") , menu=pystray.Menu(
        pystray.MenuItem(
            'Update Now',
            lambda icon, item: runupd(icon)),
        pystray.MenuItem(
            'View Log',
            lambda icon, item: showpg("",icon)),
        pystray.MenuItem(
            'Settings',
            lambda icon, item: showpg("settings",icon)),
        pystray.MenuItem(
            'Version ' + utils.vers,
            lambda icon, item: about(icon)),
        pystray.MenuItem(
            'Quit',
            lambda icon, item: exit_action(icon)))
    ).run(setup=main)