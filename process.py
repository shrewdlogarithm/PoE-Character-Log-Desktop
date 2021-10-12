import os,re,time,traceback,requests,json
import utils,charparser

# CLIENTLOG
lastlogfile = 0
lastlogdate = 0

def checklog():
    global lastlogdate,lastlogfile
    if os.path.exists(utils.getopt("clientlog")):
        upd = os.stat(utils.getopt("clientlog")).st_mtime
        if upd != lastlogfile:
            f = open(utils.getopt("clientlog"), "rb")
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(0-min(size,65535),os.SEEK_END)
            for line in f.readlines():
                try:
                    line = line.decode('utf-8')
                    logln = re.search("^([0-9]{4})/([0-9]{2})/([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2}) ([0-9]+?) (.*)$",line)
                    if logln:
                        newlog = False
                        if lastlogdate == 0:
                            newlog = True
                        else:
                            for dp in range(0,6):
                                if int(logln.groups()[dp]) > int(lastlogdate[dp]):
                                    newlog = True
                                    break
                                elif int(logln.groups()[dp]) < int(lastlogdate[dp]):
                                    break                            
                        if lastlogdate != 0 and newlog:
                            zonedf = re.search("Generating level ([0-9]+) area \"(.*)\"",logln.groups()[7])
                            if zonedf:
                                utils.writelog(zonedf.groups()[1] + " (" + zonedf.groups()[0] + ")")   
                                loadprofile()
                        lastlogdate = logln.groups()
                except:
                    utils.writelog("Error decoding PoE Log")            
            f.close()
        lastlogfile = upd
    else:
        utils.writelog("Path to client.txt log file invalid/not found")

# PROFILE
poesite = 'https://www.pathofexile.com'
session = requests.Session()
session.headers.update({'User-Agent': 'POEClog'})

xpthresh = [0,525,1760,3781,7184,12186,19324,29377,43181,61693,85990,117506,157384,207736,269997,346462,439268,
551295,685171,843709,1030734,1249629,1504995,1800847,2142652,2535122,2984677,3496798,4080655,4742836,5490247,6334393,
7283446,8384398,9541110,10874351,12361842,14018289,15859432,17905634,20171471,22679999,25456123,28517857,31897771,
35621447,39721017,44225461,49176560,54607467,60565335,67094245,74247659,82075627,90631041,99984974,110197515,121340161,
133497202,146749362,161191120,176922628,194049893,212684946,232956711,255001620,278952403,304972236,333233648,363906163,
397194041,433312945,472476370,514937180,560961898,610815862,664824416,723298169,786612664,855129128,929261318,1009443795,
1096169525,1189918242,1291270350,1400795257,1519130326,1646943474,1784977296,1934009687,2094900291,2268549086,2455921256,
2658074992,2876116901,3111280300,3364828162,3638186694,3932818530,4250334444]

def getlvlprog(lvl,xp):
    totlvl = xpthresh[int(lvl)] - xpthresh[int(lvl)-1]
    sofarlvl = int(xp) - int(xpthresh[int(lvl)-1])
    return "L%s %s" % (lvl,str(int(sofarlvl/(totlvl/100)))+"%")

def getprofile():
    account = utils.getopt("account")
    return session.get(f"{poesite}/character-window/get-characters?accountName={account}&realm=pc")

lastch = ""
olddb = {}

def loadprofile():
    global lastch,olddb
    if time.time() - utils.getopt("lastapi") > 5:
        apichars = getprofile()
        if apichars.status_code == 200:
            apichardb = apichars.json()
            for chr in apichardb:
                for ochr in olddb:
                    if ochr["name"] == chr["name"] and chr["experience"] != ochr["experience"]:
                        utils.writelog("%s From %s -> %s" % (chr["name"],getlvlprog(ochr["level"],ochr["experience"]),getlvlprog(chr["level"],chr["experience"])))
                        updatelog(chr["name"]) # this is the ONLY place we can be sure of the actively played character...
            for chr in apichardb:
                if "lastActive" in chr and lastch != chr["name"]:
                    lastch = chr["name"]                    
                    utils.writelog("Last Active " + lastch + "(" + str(chr["level"]) + ")")
                    break
            olddb = apichardb
        else:
            utils.writelog("PoE Account missing/not found or private?")
        utils.setopt("lastapi",time.time())

def addlog(account,chrname,data):
    data["update"] = time.time()
    chardata = [data]
    dbname = f'data/{account}-{chrname}.json'
    if os.path.exists(dbname):
        with open(dbname) as json_file:
            chardata = json.load(json_file)
    chardata.append(data)
    if len(chardata) > 1:
        accounts = {}
        if os.path.exists(utils.accountdb):
            with open(utils.accountdb) as json_file:
                accounts = json.load(json_file)
        charparser.makelogs(account, chrname, chardata[len(chardata)-2], chardata[len(chardata)-1])
        if not account in accounts:
            accounts[account] = {}
        accounts[account][chrname] = chardata[len(chardata)-1]["character"]
        accounts[account][chrname]["clogextradata"] = charparser.makexml(account, chrname, chardata)     
        with open(utils.accountdb, 'w') as json_file:
            json.dump(accounts, json_file, indent=4, default=str)    
    with open(dbname, 'w') as json_file:
        json.dump(chardata, json_file, indent=4, default=str)

def updatelog(chrname):
    try:        
        passives = session.get(f'{poesite}/character-window/get-passive-skills?reqData=0&accountName={utils.getopt("account")}&realm=pc&character={chrname}')
        passivedb = passives.json()
        payload = {'accountName':utils.getopt("account"), 'character': chrname}
        items = session.get(url = f'{poesite}/character-window/get-items' , params = payload)
        itemdb = items.json()
        addlog(
            utils.getopt("account"),chrname, 
            {                
                "character": itemdb["character"],
                "items": itemdb["items"],
                "passives": passivedb["hashes"]
            })        
    except:
        track = traceback.format_exc()
        print(track)