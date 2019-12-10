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
                    filename='../../log/t86_{:%Y-%m-%d}.log'.format(datetime.now()))
                    #filename='/python/log/t86_{:%Y-%m-%d}.log'.format(datetime.now()))

bDate = sys.argv[1]
eDate = sys.argv[2]
type = sys.argv[3]

model = False
if len(sys.argv) >= 5:
    if len(sys.argv[4]) == 1:
        model = True

if model:
    print("model = true")
client = pymongo.MongoClient("mongodb://172.18.0.2:27017")
#client = pymongo.MongoClient("mongodb://192.168.1.5:27017")
db = client["twStock"]
db.authenticate("twstock", "twstock123")
collRT = db["TWSE"]
collname = ""

if model:
    if type == 't86':
        collname = "t86_bak"
    else:
        collname = "stockDay_bak"
else:
    if type == 't86':
        collname = "t86"
    else:
        collname = "stockDay"
collT86 = db[collname]

datelist = pd.date_range(bDate, eDate).strftime("%Y%m%d")

proxList = ['home', 'home'
 , '59.149.159.230:8888'
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
proxidx = 1
runProxy = {}
errorProxy = {}
emptyData = False

logging.info("============" + bDate + ", " + eDate + "============")
try:
    for date in datelist:
        if type == 't86' and int(date) < 20120501 and date[-2:] != '01':
            continue
        logging.info("date = " + date)

        cnt = 0
        while cnt < 20:
            #取得代理伺服器
            if proxList[proxidx] != ' ' and proxList[proxidx] != 'home':
                proxies = {"http": proxList[proxidx]}
            else:
                proxies = {}
                
            if proxList[proxidx] in runProxy:
                runProxy[proxList[proxidx]] = runProxy[proxList[proxidx]] + 1
            else:
                runProxy[proxList[proxidx]] = 1
                errorProxy[proxList[proxidx]] = 0
            logging.debug("    prox server = " + proxList[proxidx] + ", cnt = " + str(proxidx))
            
            if type == 't86':
                r = twstock.t86.get('ALL', date, 'json', proxies, logging)
            else:
                r = twstock.t86.STOCK_DAY('ALLBUT0999', date, 'json', proxies, logging)
            
            if 'data' in r:
                data = r['data']
                for h in data:
                    query = {"code":h['code'],"date":h['date']}
                    gcode = collRT.find_one({'code':h['code']})
                    if gcode is not None and 'groupCode' in gcode:
                        h['groupCode'] = gcode['groupCode']
                    else:
                        h['groupCode'] = '00'
                    value = { "$set": h }
                    collT86.update_one(query, value, upsert=True)
                cnt = 21
                proxidx = (proxidx + 1) % len(proxList)
                logging.info("    t86 get sleep 5")
            elif 'rtcode' in r and r['rtcode'] == -1:
                cnt = 21
                #logging.error("date: " + date)
                logging.error("   " + r['rtmessage'])
                if r['rtmessage'] == 'Empty Query.':
                    emptyData = True
                    break
            else:
                #logging.error("date: " + date)
                #logging.error("groupCode: " + code)
                logging.error("   " + str(r))
                errorProxy[proxList[proxidx]] = errorProxy[proxList[proxidx]] + 1
                
                time.sleep(1)
                cnt = cnt + 1
                proxidx = (proxidx + 1) % len(proxList)
        else:
            if cnt == 20:
                logging.error("    groupCode = " + code + " had not get data")
                
        #if first massage is Empty Query then break this date
        if emptyData:
            emptyData = False
            logging.error("   break the date = " + date)

        time.sleep(1)
        
    for p in [ v for v in sorted(errorProxy.items(), key=lambda d: d[1])]:
        logging.info(str(p) + ", run = " + str(runProxy[p[0]]))
    #排序
    #[(k,di[k]) for k in sorted(di.keys())]
    #[ v for v in sorted(di.values())]
    #sorted(d.items(), lambda x, y: cmp(x[1], y[1])), 或反序： 
    #sorted(d.items(), lambda x, y: cmp(x[1], y[1]), reverse=True) 
except BaseException as e:
    logging.error("   BaseException:" + str(e))