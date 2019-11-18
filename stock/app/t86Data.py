#!/usr/bin/python
import twstock
import pymongo
import time
import sys
import pandas as pd

bDate = sys.argv[1]
eDate = sys.argv[2]
groupCode=""
if len(sys.argv) >= 4:
    groupCode = sys.argv[3]

group = []

client = pymongo.MongoClient("mongodb://172.18.0.2:27017")
db = client["twStock"]
db.authenticate("twstock", "twstock123")
collRT = db["TWSE"]
collT86 = db["t86"]

if groupCode:
    group = [groupCode]
else:
    #抓群組代碼
    group = collRT.distinct('groupCode')
print(group)
#bDate = '20190601'
#eDate = '20190630'
datelist = pd.bdate_range(bDate, eDate).strftime("%Y%m%d")
for date in datelist:
    print(date)
    for code in group:
        print("  " + code)
        cnt = 0
        while cnt < 10:
            r = twstock.t86.get(code, date, 'json')
            if 'data' in r:
                data = r['data']
                for h in data:
                    query = {"code":h['code'],"date":h['date']}
                    value = { "$set": h }
                    collT86.update_one(query, value, upsert=True)
                cnt = 10
            else:
                print(r)
                time.sleep(300)
                cnt = cnt + 1
        time.sleep(30)