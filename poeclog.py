import os,time,threading,pystray,webbrowser,pyperclip
from PIL import Image
import server,process,utils
import mapparser

runprocess = True

# Clipboard Thread
def watchclip(icon):
    global runprocess
    while runprocess == True:      
        try:
            clip = pyperclip.waitForNewPaste(5)
            mapparser.decodemap(clip)
        except:
            pass
    print("clipboard scan ending")

# Process Thread
def doprocess(icon):
    global runprocess
    process.loadprofile() # catch-up any characters/find the last active one
    while runprocess == True:        
        process.checklog()        
        time.sleep(5)
    print("process ending")

# Main Thread
def main(icon):   
    icon.visible = True

    cthread = threading.Thread(target=watchclip,args=[icon])
    cthread.start()

    pthread = threading.Thread(target=doprocess,args=[icon])
    pthread.start()

    server.start() # this is blocking

    print("main ending")

    cthread.join() # wait for thread
    pthread.join() # wait for thread

    os._exit(0) # this ensures nothing gets left behind!

# Tray Setup 
def runupd(icon):
    global runprocess
    process.loadprofile()

def showpg(pg,icon):
    webbrowser.open("http://localhost:8080/" + pg)

def about(icon):
    webbrowser.open("https://github.com/shrewdlogarithm/" + utils.homep)

def exit_action(icon):
    global runprocess
    runprocess = False
    server.stop()

pystray.Icon('Icon', Image.open(utils.base_path + "poe.png") , menu=pystray.Menu(
        pystray.MenuItem(
            'Update Now',
            lambda icon, item: runupd(icon)),
        pystray.MenuItem(
            'View Characters',
            lambda icon, item: showpg("",icon)),
        pystray.MenuItem(
            'View Log',
            lambda icon, item: showpg("log",icon)),
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