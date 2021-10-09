import glob,json,os,traceback
from charparser import makelogs,makexml

logs = glob.glob(f'logs/*-*.*')
for log in logs:
    os.remove(log)
xmls = glob.glob(f'pob/builds/*-*.*')
for xml in xmls:
    os.remove(xml)

POEChars = glob.glob('data/*.json')

for POEChar in POEChars:

    account,char = os.path.basename(POEChar).replace(".json","").split("-")

    with open(POEChar, encoding='utf-8') as json_file:
        try:
            chardata = json.load(json_file)
            for i in range(1,len(chardata)):
                makelogs(account,char, chardata[i-1], chardata[i])
        except Exception as e:
            print("Error parsing character")
            track = traceback.format_exc()
            print(track)