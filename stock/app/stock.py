#!/usr/bin/python
#print("twStockTest")
import twstock
import pymongo
import time
import sys
import logging
import requests
import random
random.seed('dogtoo')
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

proxList = ['59.149.159.230:8888'
 , '23.101.2.247:81'
 , '188.166.119.186:80'
 , '178.62.232.215:8080'
 , '192.81.223.236:3128'
 , '62.33.207.197:3128'
 , '62.33.207.202:80'
 , '58.233.211.104:443'
 , '58.233.211.104:80'
 , '109.86.229.189:8080'
 , '51.158.178.67:3128'
 , '51.158.68.26:8811'
 , '51.158.106.54:8811'
 , '58.233.211.104:80'
 , '58.233.211.104:443'
 , '23.237.173.102:3128'
 , '167.172.140.184:3128'
 , '167.172.225.187:3128'
 , '167.172.225.187:8080'
 , '51.158.68.133:8811'
 , '51.158.98.121:8811'
 , '163.172.147.94:8811'
 , '136.243.47.220:3128'
 , '23.101.2.247:81'
 , '159.138.1.185:80'
 , '194.167.44.91:80'
 , '51.158.120.84:8811'
 , '51.158.98.121:8811'
 , '163.172.152.52:8811'
 , '163.172.136.226:8811'
 , '51.158.111.229:8811'
 , '51.158.68.68:8811'
 , '163.172.147.94:8811'
 , '51.158.99.51:8811'
 , '51.158.119.88:8811'
 , '34.90.113.143:3128'
 , '141.125.82.106:80'
 , '138.201.72.117:80'
 , '185.125.204.68:3128'
 , '103.226.213.156:8888'
 , '176.123.61.238:3128'
 , '62.33.207.201:3128'
 , '150.109.162.73:3128'
 , '67.63.33.7:80'
 , '167.71.132.188:8080'
 , '157.245.207.190:8080'
 , '178.62.232.215:8080'
 , '192.81.223.236:3128'
 , '80.234.38.44:3128'
 , '109.174.19.134:8385'
 , '51.68.189.52:3128'
 , '47.74.44.84:8080'
 , '47.52.32.109:80'
 , '35.235.75.244:3128'
 , '47.52.225.33:80'
 , '157.245.196.253:8080'
 , '159.65.87.167:8080'
 , '149.28.141.62:8118'
 , '167.88.117.209:8080'
 , '47.52.131.183:80'
 , '206.189.200.179:8080'
 , '159.65.109.226:8080'
 , '167.71.138.113:8080'
 , '165.22.241.186:8080'
 , '209.97.128.45:8080'
 , '165.22.254.99:3128'
 ]

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
proxidx = 0
proxies = {}

while getSession:
    try:
        if runGroupStr != '01|02':
            proxies = {"http": random.sample(proxList, k=1)[0]}
        else:
            proxies = {}
        req = requests.Session()
        req.get(SESSION_URL, proxies=proxies, timeout=(1, 2))
        getSession = False
    except BaseException as e:
        logging.error("get Session Exception :" + str(e))
        time.sleep(10)
        if not chkRun(0):
            sys.exit(0)

while run:
    sleep = 5 #間隔5秒
    b = time.time()
    stock = twstock.realtime.get(stockCodeL, req, proxies, logging)
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
        proxies = {"http": random.sample(proxList, k=1)[0]}
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

