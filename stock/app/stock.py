#!/usr/bin/python
#print("twStockTest")
import twstock
import pymongo
import time
import sys
import logging
import requests
from datetime import timedelta, date, datetime

debug = False 
stockName = sys.argv[1]
runGroupStr = ""
if len(sys.argv) == 3:
    runGroupStr = sys.argv[2]

if len(runGroupStr) == 0:
    debug = True
    runGroupStr = "24" 

SESSION_URL = 'http://163.29.17.179/stock/index.jsp'

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s : %(message)s',
                    datefmt='%Y-%m-%dT %H:%M:%S',
                    #filename='../../log/' + stockName + '_' + '{:%Y-%m-%d}'.format(datetime.now()) + '_' + '{}.log'.format(runGroupStr.replace("|","_")) )
                    filename='/python/log/' + stockName + '_' + '{:%Y-%m-%d}'.format(datetime.now()) + '_' + '{}.log'.format(runGroupStr.replace("|","_")) )
    
client = pymongo.MongoClient("mongodb://172.18.0.2:27017")
#client = pymongo.MongoClient("mongodb://192.168.1.5:27017")
db = client["twStock"]
db.authenticate("twstock", "twstock123")

collname = ""
if debug:
    collname = "realtime_bak"
else:
    collname = "realtime"
collRT = db[collname]
collSt = db[stockName]
#runGroupSet = set(runGroupStr.split(","))

#每日下午13:31分為止
"""
localtime = time.localtime() # get struct_time
today = time.strftime("%Y%m%d", localtime)

localtime = int(time.mktime(localtime)) #系統時間
strtime = int(time.mktime(time.strptime(today + ' 00:50:00', '%Y%m%d %H:%M:%S'))) # 8:50 起
endtime = int(time.mktime(time.strptime(today + ' 05:32:00', '%Y%m%d %H:%M:%S'))) # 13:30 結束
twoEndtime = int(time.mktime(time.strptime(today + ' 06:50:00', '%Y%m%d %H:%M:%S'))) # 14:30 
"""
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


"""
localtime = time.localtime() # get struct_time
today = time.strftime("%Y%m%d", localtime)

localtime = int(time.mktime(localtime)) #系統時間
strtime = int(time.mktime(time.strptime(today + ' 00:50:00', '%Y%m%d %H:%M:%S'))) # 8:50 起
endtime = int(time.mktime(time.strptime(today + ' 05:32:00', '%Y%m%d %H:%M:%S'))) # 13:30 結束
twoEndtime = int(time.mktime(time.strptime(today + ' 06:50:00', '%Y%m%d %H:%M:%S'))) # 14:30 
"""
def chkRun(runcnt):
    sysTime = int( '{:%d%H%M}'.format(datetime.now()) )
    # 9:00 起
    strTime = int( '{:%d}'.format(datetime.now()) + '0859' )
    # 13:40 結束
    endTime = int( '{:%d}'.format(datetime.now()) + '1340' )
    # 15:00 零股結算
    secBTime = int( '{:%d}'.format(datetime.now()) + '1459' )
    secETime = int( '{:%d}'.format(datetime.now()) + '1510' )
    logging.debug("sysTime = " + str(sysTime) + ", strTime = " + str(strTime) + ", endTime = " + str(endTime) + ", secBTime = " + str(secBTime) + ", secETime = " + str(secETime))
    if runcnt == 0 and debug:
        return True
    elif runcnt == 1 and debug:
        return False
    elif sysTime > strTime and sysTime < endTime:
        return True
    elif sysTime > secBTime and sysTime < secETime:
        return True
    else:
        return False

#print("***" + time.ctime() + "*** (", len(stockCodeL), ")", flush=True)
#logging.error("***" + '{:%H:%M:%S}'.format(datetime.now()) + "*** " + runGroupStr + " (" + str(len(stockCodeL)) + ")")
logging.info(" gropuCode = " + runGroupStr + "(cnt = " + str(len(stockCodeL)) + ")")
run = True
run = chkRun(0)
#while (localtime >= strtime and localtime <= endtime) or debug == True or (localtime > endtime and localtime <= twoEndtime):
getSession = True
while getSession:
    try:
        req = requests.Session()
        req.get(SESSION_URL, timeout=(1, 2))
        getSession = False
    except BaseException as e:
        logging.error("get Session Exception :" + str(e))
        time.sleep(10)
        if not chkRun(0):
            sys.exit(0)

while run:
    sleep = 5 #間隔5秒
    b = time.time()
    stock = twstock.realtime.get(stockCodeL, req, logging)
    #print(runGroupStr,stock["success"])
    if stock["success"]:
        logging.info("    success")
        #轉換格式
        logcnt = 0;
        for code, v in stock.items():
            logcnt = logcnt + 1;
            if isinstance(v, dict) and v['success']:
                try:
                    del v['info']
                    rlTime = v['realtime']
                    del v['realtime']
                    v.update(rlTime)
                    v.update({'group':group[v['code']][0:2]})
                    #存入db
                    #collRT.insert_one(v)
                    #新的訊息有可能沒有交易，新增一筆的方式是要張數有增加
                    query = {"code":v['code'],"date":v['date'],"accumulate_trade_volume":{"$gte":v['accumulate_trade_volume']}}
                    value = { "$set": v}
                    if logcnt == 1:
                        logging.debug("        db inst beg")
                        
                    if "final_trade_volume" not in v:
                        if logcnt == 1:
                            logging.debug("        " + str({"accumulate_trade_volume":v['accumulate_trade_volume']
                                                          , "trade_volume":v['trade_volume']} )
                                         )
                        collRT.update_one(query, value, upsert=True)
                    else:
                        query = {"code":v['code'],"date":v['date'],"final_trade_volume":v['final_trade_volume']}
                        if logcnt == 1:
                            logging.debug("        " + str({"final_trade_volume":v['final_trade_volume']
                                                          , "trade_volume":v['trade_volume']}))
                        value = {"$set":v}
                        collRT.update_one(query, value, upsert=True)
                        
                    if logcnt == 1:
                        logging.debug("        db inst end")
                except BaseException as e:
                    logging.error("    BaseException :" + str(e))
    else:
        logging.error("    error" + stock['rtmessage'])
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
    run = chkRun(1)
    
    #localtime = int(time.mktime(time.localtime()))
    e = time.time()
    sleep = sleep - (e-b) #間隔時間含有執行時間
    if sleep > 0:
        time.sleep(sleep)
    #print("===" + time.ctime() + "===", e-b, flush=True)
else:
    logging.info("time out")
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

