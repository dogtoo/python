#!/usr/bin/python
#print("twStockTest")
import twstock
import pymongo
import time
import sys
debug = False 
stockName = sys.argv[1]
runGroupStr = sys.argv[2]
if len(runGroupStr) == 0:
    debug = True
    runGroupStr = "24" 
client = pymongo.MongoClient("mongodb://172.18.0.2:27017")
db = client["twStock"]
db.authenticate("twstock", "twstock123")
collRT = db["realtime"]
collSt = db[stockName]
#runGroupSet = set(runGroupStr.split(","))

#每日下午13:31分為止
localtime = time.localtime() # get struct_time
today = time.strftime("%Y%m%d", localtime)

localtime = int(time.mktime(localtime)) #系統時間
strtime = int(time.mktime(time.strptime(today + ' 00:50:00', '%Y%m%d %H:%M:%S'))) # 8:50 起
endtime = int(time.mktime(time.strptime(today + ' 05:32:00', '%Y%m%d %H:%M:%S'))) # 13:30 結束
twoEndtime = int(time.mktime(time.strptime(today + ' 06:50:00', '%Y%m%d %H:%M:%S'))) # 14:30 
#print("localtime:", localtime, ", Str time:", strtime, ", End time:", endtime, flush=True)

group = {}
stockCodeL = []
qurySt = collSt.find({'groupCode':{'$regex':runGroupStr}}, {"_id": 0, "code":1, "groupCode":1})
for st in qurySt:
    if st['groupCode'] == '00':
        continue
    stockCodeL.append(st['code']) #這次要查的股票們
    group[st['code']] = st['groupCode'] #用股票號碼回頭找group
    """
    #查詢股票群組
    for stockCName,codeL in st.items():
        stockCodeL = []
        if stockCName == "OTHER":
            continue
        #同組股票代碼
        stockGroupCode = "00"
        for code,t in codeL.items():
            if 'groupCode' in t:
                stockGroupCode = t["groupCode"]
            stockCodeL.append(code)
        #只跑指定的組
        if stockGroupCode not in runGroupSet:
            continue
        group[stockGroupCode]=stockCodeL
        print(stockCName + "(" + stockGroupCode + ")" + " " + str(len(stockCodeL)), flush=True)
    """

print("***" + time.ctime() + "*** (", len(stockCodeL), ")", flush=True)
while (localtime >= strtime and localtime <= endtime) or debug == True or (localtime > endtime and localtime <= twoEndtime):
    sleep = 5 #間隔5秒
    b = time.time()
    stock = twstock.realtime.get(stockCodeL)
    #print(runGroupStr,stock["success"])
    if stock["success"]:
        #轉換格式
        for code, v in stock.items():
            if isinstance(v, dict) and v['success']:
                del v['info']
                rlTime = v['realtime']
                del v['realtime']
                v.update(rlTime)
                v.update({'group':group[v['code']][0:2]})
                #存入db
                #collRT.insert_one(v)
                #新的訊息有可能沒有交易，新增一筆的方式是要張數有增加
                query = {"code":v['code'],"date":v['date'],"accumulate_trade_volume":{"$gte":v['accumulate_trade_volume']}}
                value = { "$set": v }
                if "final_trade_volume" not in v:
                    collRT.update_one(query, value, upsert=True)
                else:
                    query = {"code":v['code'],"date":v['date'],"final_trade_volume":v['final_trade_volume']}
                    value = {"$set":v}
                    collRT.update_one(query, value, upsert=True)
    """
    #查詢股票群組
    for stockGroupCode,codeL in group.items():
        #取得股票即時資料
        b = int(time.mktime(time.localtime()))
        stock = twstock.realtime.get(codeL)
        if stock["success"]:
            #轉換格式
            for code, v in stock.items():
                if isinstance(v, dict):
                    del v['info']
                    rlTime = v['realtime']
                    del v['realtime']
                    v.update(rlTime)
                    v.update({'group':stockGroupCode})
                    #存入db
                    #collRT.insert_one(v)
                    query = {"code":v['code'],"timestamp":v['timestamp']}
                    value = { "$set": v }
                    collRT.update_one(query, value, upsert=True)
    e = localtime
    print(stockGroupCode, ":", e-b, flush=True)
    """
    
    localtime = int(time.mktime(time.localtime()))
    e = time.time()
    sleep = sleep - (e-b) #間隔時間含有執行時間
    if sleep > 0:
        time.sleep(sleep)
    #print("===" + time.ctime() + "===", e-b, flush=True)
#print(time.ctime());
"""
python3 stock.py TWSE 01,02,20
python3 stock.py TWSE 03,21,12
python3 stock.py TWSE 04,18,14
python3 stock.py TWSE 28
python3 stock.py TWSE 05,22
python3 stock.py TWSE 06,08,09
python3 stock.py TWSE 10,11
python3 stock.py TWSE 15,25
python3 stock.py TWSE 24
python3 stock.py TWSE 31,27
python3 stock.py TWSE 26,29,39
python3 stock.py TWSE 23,16,17
"""

