import re
import utils

lastmap = ""

def decodemap(maptext):
    global lastmap
    if lastmap != maptext:
        map = {
            "Name": "",
            "Rarity": "",
            "Map Tier": 0,
            "Item Quantity": 0,
            "Item Rarity": 0,
            "Monster Pack Size": 0,
            "Quality": 0,
            "Corrupted": False,
            "Identified": True,
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
                            if map["Rarity"] == "Magic":
                                ln = re.sub(r'^[^ ]+ ',"",ln)
                            map["Name"] = ln.replace(" Map","").replace("Superior ","")
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
                                tokval = int(numval.groups()[0])
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
                            if len(ln) > 2:
                                map["Modifiers"].append(ln)
            print(map)
            mapstub = map["Name"] + " T" + map["Map Tier"] 
            if map["Item Quantity"] > 0:
                mapstub += f' Qt:{map["Item Quantity"]}'
            if map["Quality"] > 0:
                mapstub += f' Ql:{map["Quality"]}'
            if not map["Identified"]:
                mapstub += " Unid"
            elif len(map["Modifiers"]) > 0:
                mapstub += f' {len(map["Modifiers"])}Mod'
            if map["Corrupted"]:
                mapstub += " Corrupt"
            utils.writelog(mapstub)
            lastmap = maptext