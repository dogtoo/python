#!/usr/bin/python
import twstock
import pymongo
import time
import sys
import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s : %(message)s',
                    datefmt='%Y-%m-%dT %H:%M:%S',
                    #filename='../../log/t86_{:%Y-%m-%d}.log'.format(datetime.now()))
                    filename='/python/log/t86_{:%Y-%m-%d}.log'.format(datetime.now()))

bDate = sys.argv[1]
eDate = sys.argv[2]
groupCode=""
model = False
if len(sys.argv) >= 4:
    if len(sys.argv[3]) == 1:
        model = True
    elif len(sys.argv[3]) == 2:
        groupCode = str(sys.argv[3])

group = []
#print("bDate = " + bDate + ", eDate = " + eDate + ", groupCode = " + groupCode)
if model:
    print("model = true")
client = pymongo.MongoClient("mongodb://172.18.0.2:27017")
#client = pymongo.MongoClient("mongodb://192.168.1.5:27017")
db = client["twStock"]
db.authenticate("twstock", "twstock123")
collRT = db["TWSE"]
collname = ""
if model:
    collname = "t86_bak"
else:
    collname = "t86"
collT86 = db[collname]

if groupCode:
    group = [groupCode]
else:
    #抓群組代碼
    group = collRT.distinct('groupCode')
logging.info("接收群組List: " + ', '.join(group))
#bDate = '20190601'
#eDate = '20190630'
datelist = pd.bdate_range(bDate, eDate).strftime("%Y%m%d")

proxList = [' ', 'home'
  , '167.99.159.6:8080'
  , '157.230.112.218:8080'
  , '167.71.103.168:3128'
  , '45.5.150.3:9090'
  , '64.74.98.214:3128'
  , '45.6.92.18:8080'
  , '184.183.3.211:8080'
  , '198.98.54.241:8080'
  , '43.245.223.35:80'
  , '219.85.125.190:80'
  , '122.201.144.219:3128'
  , '106.104.12.180:80'
  , '220.130.205.58:8080'
  , '59.120.72.249:8080'
  , '118.163.13.200:8080'
  , '114.32.215.139:8080'
  , '118.171.24.73:3128'
  , '118.171.24.171:3128'
  , '198.98.58.178:8080'
  , '50.235.149.74:8080'
  , '139.180.129.160:8888'
  , '154.7.2.121:3129'
  , '154.7.5.53:3129'
  , '154.7.2.238:3129'
  , '154.7.2.253:3129'
  , '192.163.215.33:443'
]
proxidx = 1
errorProxy = {}

logging.info("============" + bDate + ", " + eDate + ", groupCode = " + groupCode + "============")
try:
    for date in datelist:
        logging.info("date = " + date)
        for code in group:
            logging.info("    groupCode = " + code)
            cnt = 0
            while cnt < 10:
                if proxList[proxidx] != ' ' and proxList[proxidx] != 'home':
                    proxies = {"http": proxList[proxidx]}
                else:
                    proxies = {}
                logging.debug("    prox server = " + proxList[proxidx] + ", cnt = " + str(proxidx))
                r = twstock.t86.get(code, date, 'json', proxies, logging)
                if 'data' in r:
                    data = r['data']
                    for h in data:
                        query = {"code":h['code'],"date":h['date']}
                        value = { "$set": h }
                        collT86.update_one(query, value, upsert=True)
                    cnt = 10
                    proxidx = (proxidx + 1) % len(proxList)
                    logging.info("    t86 get sleep 5")
                elif 'rtcode' in r and r['rtcode'] == -1:
                    cnt = 10
                    #logging.error("date: " + date)
                    logging.error("   " + r['rtmessage'])
                else:
                    #logging.error("date: " + date)
                    #logging.error("groupCode: " + code)
                    logging.error("   " + str(r))
                    if proxList[proxidx] in errorProxy:
                        errorProxy[proxList[proxidx]] = errorProxy[proxList[proxidx]] + 1
                    else:
                        errorProxy[proxList[proxidx]] = 1
                        
                    time.sleep(1)
                    cnt = cnt + 1
                    proxidx = (proxidx + 1) % len(proxList)
            time.sleep(5)

    for p in [ v for v in sorted(errorProxy.items(), key=lambda d: d[1])]:
        logging.info(p)

"""       
排序
[(k,di[k]) for k in sorted(di.keys())]
[ v for v in sorted(di.values())]
sorted(d.items(), lambda x, y: cmp(x[1], y[1])), 或反序： 
sorted(d.items(), lambda x, y: cmp(x[1], y[1]), reverse=True) 
"""
except BaseException as e:
    logging.error("   " + str(e))