#!/usr/bin/python
print("twStockTest");
import twstock
import pymongo
import time
client = pymongo.MongoClient("mongodb://172.17.0.3:27017")
db = client["twStock"] 
db.authenticate("twstock", "twstock123")
collRT = db["realtime"]
colltpexG = db["TPEX"]
#print(time.ctime());
tpex = []
tpexG = colltpexG.find({}, {"_id": 0})
#comidAry = ['2330','2105']
#while timestamp < 1330000000:
for x in tpexG:
    for k,data in x.items():
        if k == "OTHER":
            continue
        print(k + " " + time.ctime())
        for code,v in data.items():
            tpex.append(code)
        stock = twstock.realtime.get(tpex)
        if stock["success"]:
            x = collRT.insert_one(stock)
        tpex.clear()
        print("===" + time.ctime() + "===")
#time.sleep(3)
#print(time.ctime());