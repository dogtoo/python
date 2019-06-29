#!/usr/bin/python
import twstock
import pymongo
import time
import sys
import pandas as pd

bDate = sys.argv[1]
eDate = sys.argv[2]
groupCode = sys.argv[3]
groupCode=""
group = []

client = pymongo.MongoClient("mongodb://172.17.0.3:27017")
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
    #print(date)
    for code in group:
        data = twstock.t86.get(code, date, 'json')['data']
        print(data)
        query = {"code":data['code'],"date":data['date']}
        value = { "$set": data }
        collT86.update_one(query, value, upsert=True)
        