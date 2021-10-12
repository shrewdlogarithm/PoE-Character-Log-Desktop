import re

lastmap = ""

def decodemap(maptext):
    global lastmap
    if lastmap != maptext:
        rarename = re.compile(r"[a-z]'s ", re.IGNORECASE)
        map = {
            "Name": "",
            "Rarity": "",
            "Map Tier": 0,
            "Item Quantity": 0,
            "Item Rarity": 0,
            "Monster Pack Size": 0,
            "Quality": 0,
            "Corrupted": False,
            "Modifiers": []
        }
        if maptext.startswith("Item Class: Maps"):
            sects = re.split(r'-{3,}\r\n',maptext)
            if len(sects) > 0:
                lns = re.split(r'\r\n',sects[0])
                for p in range(0,len(lns)-1):
                    ln = lns[p]
                    rari = re.match(r'Rarity: (.*)$',ln)
                    if rari:
                        map["Rarity"] = rari.groups()[0]
                    if ln.endswith(" Map"):
                        if map["Rarity"] == "Unique":
                            map["Name"] = lns[p-1] 
                        else:
                            map["Name"] = re.sub(r"[a-z]+'s ","",ln.replace(" Map","").replace("Superior ",""), flags=re.IGNORECASE)
            if len(sects) > 1:
                lns = re.split(r'\r\n',sects[1])
                for ln in lns:
                    toks = re.match(r'(.*?): (.*)$',ln)
                    if toks:
                        tok = toks.groups()[0]
                        if tok in map:
                            tokval = toks.groups()[1]
                            numval = re.search(r'([0-9]+)+%',tokval)
                            if numval:
                                tokval = numval.groups()[0]
                            map[tok] = tokval
            if len(sects) > 2:
                numval = re.search(r'Item Level: ([0-9]+)\r\n',sects[2])
                map["Item Level"] = numval.groups()[0]
            if len(sects) > 3:
                for sc in range(3,len(sects)-1):
                    if sects[sc].startswith("Corrupted"):
                        map["Corrupted"] = True
                    elif sects[sc].startswith("Unidentified"):
                        map["Identified"] = False
                    elif not sects[sc].startswith("Travel to") and (map["Rarity"] != "Unique" or sc < 4): # ignore blurbs
                        lns = re.split(r'\r\n',sects[sc])
                        for ln in lns:
                            infl = re.search(r'influenced by ([^\(\r]+)',ln)
                            if infl:
                                map["Influenced"] = infl.groups()[0].strip()
                                continue
                            occu = re.search(r'occupied by ([^\(\r]+)',ln)
                            if occu:
                                map["Occupied"] = occu.groups()[0].strip()
                                continue
                            map["Modifiers"].append(ln)
            print(map)
            lastmap = maptext