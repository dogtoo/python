#!/usr/bin/python
print("twStockTest")
import twstock
import pymongo
import time
import sys

stockName = sys.argv[1]
runGroupStr = sys.argv[2]
client = pymongo.MongoClient("mongodb://172.18.0.2:27017")
db = client["twStock"]
db.authenticate("twstock", "twstock123")
collRT = db["realtime"]
collSt = db[stockName]
runGroupSet = set(runGroupStr.split(","))

#每日下午13:31分為止
timestamp = 0
localtime = time.localtime() # get struct_time
today = time.strftime("%Y%m%d", localtime)

localtime = int(time.mktime(localtime)) #系統時間
strtime = int(time.mktime(time.strptime(today +  01:00:00, %Y%m%d %H:%M:%S))) # 9:00 起
endtime = int(time.mktime(time.strptime(today +  05:30:00, %Y%m%d %H:%M:%S))) # 13:30 結束
print("localtime:", localtime, ", Str time:", strtime, ", End time:", endtime, flush=True)

#抓出所有群組
group = {}
qurySt = collSt.find({}, {"_id": 0})
for st in qurySt:
    #查詢股票群組
    for stockCName,codeL in st.items():
        stockCodeL = []
        if stockCName == "OTHER":
            continue
        #同組股票代碼
        stockGroupCode = "00"
        for code,t in codeL.items():
            if groupCode in t:
                stockGroupCode = t["groupCode"]
            stockCodeL.append(code)
        #只跑指定的組
        if stockGroupCode not in runGroupSet:
            continue
        group[stockGroupCode]=stockCodeL
        print(stockCName + "(" + stockGroupCode + ")" + time.ctime(), flush=True)

while localtime >= strtime and timestamp <= endtime:
    print("***" + time.ctime() + "***", flush=True)
    #查詢股票群組
    for stockGroupCode,codeL in group.items():
        #取得股票即時資料
        stock = twstock.realtime.get(codeL)
        if stock["success"]:
            #轉換格式
            for code, v in stock.items():
                if isinstance(v, dict):
                    del v[info]
                    rlTime = v[realtime]
                    del v[realtime]
                    v.update(rlTime)
                    v.update({group:stockGroupCode})
                    #存入db
                    #collRT.insert_one(v)
                    query = {"code":v[code],"timestamp":v[timestamp]}
                    value = { "$set": v }
                    collRT.update_one(query, value, upsert=True)
                    timestamp = int(v[timestamp])
    print("===" + time.ctime() + "===", flush=True)
    print("timestamp = " + str(timestamp))
#print(time.ctime());
