import sys,os,json
from datetime import datetime

homep = "https://github.com/shrewdlogarithm/PoE-Character-Log-Desktop"
vers = "0.315.01"

# create directories
dirs = ("data","logs","pob","pob/builds")
for dir in dirs:
    try:
        if not os.path.exists(dir):
            raise
    except:
        os.mkdir(dir)


# Pyinstaller --onefile data directory handler
base_path = ""
try:
    base_path = sys._MEIPASS + "\\"
except Exception:
    base_path = os.path.abspath(".") + "\\"

# OPTIONS
options = {}

def getopt(opt):
    global options
    if opt in options:
        return options[opt]
    else:
        return 0

def setopt(opt,val):
    global options
    options[opt] = val
    saveopt()

def saveopt():
    global options
    with open('settings.json', 'w') as outfile:
        json.dump(options, outfile, sort_keys=True, indent=4)

try:
    with open('settings.json') as json_file:
        options = json.load(json_file)
except:
    options = {
        "clientlog": "path to POE/logs/client.txt goes here",
        "account": "your POE account name - login NOT character - goes here"
    }
    saveopt()

# OUTPUT
def writelog(line):
    now = datetime.now()
    f = open("poeclog.log", "a")
    f.writelines(now.strftime("%d/%m/%Y, %H:%M:%S") + " " + line + "\n")
    print(line)
    f.close()

def getlogs():
    f = open("poeclog.log","r")
    logs = f.readlines()
    f.close()
    return logs
