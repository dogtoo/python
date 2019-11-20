#!/usr/bin/python
import twstock
import pymongo
import time
import sys
import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.WARNING,
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

proxList = ['', 'home', 
    '43.245.223.35:80'
  , '219.85.125.190:80'
  , '122.201.144.219:3128'
 # , '106.104.12.180:80'
 # , '220.130.205.58:8080'
  , '59.120.72.249:8080'
 # , '118.163.13.200:8080'
  , '114.32.215.139:8080'
  , '118.171.24.73:3128'
  , '118.171.24.171:3128'
]
proxidx = 1

logging.error("============" + bDate + ", " + eDate + ", groupCode = " + groupCode + "============")
try:
    for date in datelist:
        logging.error("date = " + date)
        for code in group:
            logging.error("    groupCode = " + code)
            cnt = 0
            while cnt < 10:
                if proxList[proxidx] != '' and proxList[proxidx] != 'home':
                    proxies = {"http": proxList[proxidx]}
                else:
                    proxies = {}
                logging.error("    prox server = " + proxList[proxidx] + ", cnt = " + str(proxidx))
                r = twstock.t86.get(code, date, 'json', proxies)
                logging.error("    t86 get")
                if 'data' in r:
                    data = r['data']
                    for h in data:
                        query = {"code":h['code'],"date":h['date']}
                        value = { "$set": h }
                        collT86.update_one(query, value, upsert=True)
                    cnt = 10
                    proxidx = (proxidx + 1) % len(proxList)
                elif 'rtcode' in r and r['rtcode'] == -1:
                    cnt = 10
                    #logging.error("date: " + date)
                    logging.error("    " + r['rtmessage'])
                else:
                    #logging.error("date: " + date)
                    #logging.error("groupCode: " + code)
                    logging.error("    error: " + str(r))
                    if model:
                        exit()
                    else:
                        time.sleep(1)
                    cnt = cnt + 1
                    proxidx = (proxidx + 1) % len(proxList)
            logging.error("sleep 5")
            time.sleep(5)
except BaseException as e:
    logging.error("    error: " + str(e))