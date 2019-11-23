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

proxList = ['home', 'home'
  , '45.55.9.218:8080'
  , '45.55.9.218:8080'
  , '45.55.27.15:8080'
  , '67.205.149.230:8080'
  , '198.199.120.102:3128'
  , '174.138.54.49:8080'
  , '206.189.229.46:3128'
  , '162.243.108.129:3128'
  , '159.203.166.41:8080'
  , '45.55.27.161:3128'
  , '165.227.215.71:8080'
  , '67.205.132.241:8080'
  , '159.203.91.6:8080'
  , '138.68.41.90:3128'
  , '45.55.23.78:3128'
  , '173.192.128.238:8123'
  , '157.245.184.172:3128'
  , '138.68.24.145:8080'
  , '138.197.204.55:8080'
  , '162.243.108.161:8080'
  , '162.243.108.141:3128'
  #, '167.99.159.6:8080'
  #, '157.230.112.218:8080'
  #, '167.71.103.168:3128'
  #, '45.5.150.3:9090'
  #, '64.74.98.214:3128'
  #, '45.6.92.18:8080'
  ##, '184.183.3.211:8080'
  , '198.98.54.241:8080'
  #, '43.245.223.35:80'
  #, '219.85.125.190:80'
  ##, '122.201.144.219:3128'
  #, '106.104.12.180:80'
  #, '220.130.205.58:8080'
  ##, '59.120.72.249:8080'
  ##, '118.163.13.200:8080'
  ##, '114.32.215.139:8080'
  #, '118.171.24.73:3128'
  #, '118.171.24.171:3128'
  #, '198.98.58.178:8080'
  #, '50.235.149.74:8080'
  ##, '139.180.129.160:8888'
  ##, '154.7.2.121:3129'
  ##, '154.7.5.53:3129'
  ##, '154.7.2.238:3129'
  ##, '154.7.2.253:3129'
  #, '192.163.215.33:443'
  #, '118.27.31.50:3128'
  #, '122.152.138.139:8080'
  #, '133.167.123.158:3128'
  #, '118.27.37.20:3128'
  #, '117.102.197.136:8080'
  , '153.127.12.227:3128'
  #, '133.18.48.68:8080'
  #, '160.238.176.205:8080'
  #, '36.55.230.146:8888'
  , '119.192.195.83:8080'
  #, '121.170.201.59:80'
  #, '121.170.201.57:80'
  , '210.107.78.173:3128'
  #, '175.125.216.117:8080'
  , '119.192.195.83:443'
  , '58.233.211.104:80'
  , '119.192.195.83:80'
  , '58.233.211.104:443'
  #, '209.90.63.108:80'
  , '208.255.161.107:8180'
  , '23.237.173.102:3128'
  #, '192.210.144.171:80'
  #, '154.7.9.8:3129'
  , '157.230.240.234:8080'
  #, '143.59.221.210:8080'
  #, '167.172.32.238:3128'
  , '81.92.202.192:80'
  , '217.182.120.164:8080'
  #, '167.172.32.223:3128'
  #, '217.182.120.160:8080'
  , '167.172.140.184:3128'
  , '167.172.225.187:3128'
  , '167.172.224.108:3128'
  , '167.172.225.187:8080'
  , '51.158.179.242:8080'
  , '51.158.108.135:8811'
  , '51.158.111.229:8811'
  , '51.158.68.133:8811'
  #, '167.172.176.91:8080'
  #, '51.75.75.87:3128'
  , '51.158.98.121:8811'
  #, '173.192.21.89:80'
  #, '165.22.40.78:80'
  #, '209.132.146.44:3128'
  #, '161.202.226.194:25'
  #, '45.32.22.176:8080'
  , '210.140.170.236:80'
  #, '45.76.215.249:8080'
  #, '45.76.199.145:8888'
  , '200.89.174.181:3128'
  , '200.89.178.63:80'
  , '200.89.178.36:3128'
  #, '200.69.67.173:9991'
  , '200.89.178.64:8080'
  #, '200.89.178.64:8811'
  , '163.172.136.226:8811'
  , '62.210.203.105:3128'
  #, '159.8.114.37:25'
  #, '159.8.114.37:8123'
  #, '45.32.144.235:8080'
  , '163.172.147.94:8811'
  , '212.47.234.231:80'
  #, '37.187.4.81:1080'
  #, '46.101.178.175:1080'
  , '136.243.47.220:3128'
  #, '136.243.47.220:808'
  , '5.9.143.59:3128'
  #, '91.205.174.26:80'
  #, '202.182.121.205:8080'
  #, '139.162.78.109:8080'
  , '124.219.176.139:39589'
  , '115.160.21.243:8080'
  , '183.111.26.15:8080'
  , '18.162.210.52:8888'
  , '119.28.74.119:8081'
  , '23.101.2.247:81'
  , '203.185.55.217:443'
  , '159.138.1.185:80'
  #, '151.80.36.115:1080'
  , '194.167.44.91:80'
  #, '92.222.180.156:8080'
  , '51.158.120.84:8811'
  , '51.158.108.135:8811'
  , '51.158.98.121:8811'
  , '163.172.189.32:8811'
  , '51.158.123.35:8811'
  , '163.172.152.52:8811'
  , '163.172.136.226:8811'
  , '51.158.111.229:8811'
  , '51.158.68.68:8811'
  , '163.172.147.94:8811'
  , '51.158.99.51:8811'
  , '51.158.119.88:8811'
  #, '212.47.249.126:8118'
  , '54.38.110.35:47640'
  #, '62.210.209.94:8118'
]
proxidx = 1
runProxy = {}
errorProxy = {}
emptyData = False

logging.info("============" + bDate + ", " + eDate + ", groupCode = " + groupCode + "============")
try:
    for date in datelist:
        logging.info("date = " + date)
        for gcode in group:
            logging.info("    groupCode = " + gcode)
            cnt = 0

            while cnt < 20:
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
                r = twstock.t86.get(gcode, date, 'json', proxies, logging)
                if 'data' in r:
                    data = r['data']
                    for h in data:
                        query = {"code":h['code'],"date":h['date']}
                        #groupCode需要在查詢中用到
                        h['groupCode'] = gcode
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
                break

            time.sleep(5)
    for p in [ v for v in sorted(errorProxy.items(), key=lambda d: d[1])]:
        logging.info(str(p) + ", run = " + str(runProxy[p[0]]))
    #排序
    #[(k,di[k]) for k in sorted(di.keys())]
    #[ v for v in sorted(di.values())]
    #sorted(d.items(), lambda x, y: cmp(x[1], y[1])), 或反序： 
    #sorted(d.items(), lambda x, y: cmp(x[1], y[1]), reverse=True) 
except BaseException as e:
    logging.error("   " + str(e))