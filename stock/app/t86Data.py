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
        groupCode = sys.argv[3]

group = []
print("bDate = " + bDate + ", eDate = " + eDate + ", groupCode = " + groupCode)
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
logging.error("============" + bDate + ", " + eDate + "============")
for date in datelist:
    logging.info("date = " + date)
    for code in group:
        logging.info("groupCode = " + code)
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
            elif 'rtcode' in r and r['rtcode'] == -1:
                cnt = 10
                logging.error("date: " + date)
                logging.error(r['rtmessage'])
            else:
                logging.error("date: " + date)
                logging.error("groupCode: " + code)
                logging.error("    error: " + str(r))
                if model:
                    exit()
                else:
                    time.sleep(300)
                cnt = cnt + 1
        time.sleep(30)