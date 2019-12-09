#!/usr/bin/python
import pymongo
import subprocess
import time
from datetime import timedelta, date, datetime
import os
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s : %(message)s',
                    datefmt='%Y-%m-%dT %H:%M:%S',
                    filename='../../log/realTime_{:%Y-%m-%d}.log'.format(datetime.now()))
                    #filename='/python/log/realTime_{:%Y-%m-%d}.log'.format(datetime.now()))

#cmd = 'python3 /python/stock/app/stock.py TWSE "{}"'
cmd = 'python ./stock.py TWSE "{}"'
cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
logging.debug("Files in '%s': %s" % (cwd, files))

#依前一天交易量決定今日程序
#10k ~ x *5
#5k ~ 9.9k *8
#2k ~ 4.9k *10
#1k ~ 1.9k *20
#y ~ 0.9k * 50
#client = pymongo.MongoClient("mongodb://172.18.0.2:27017")
client = pymongo.MongoClient("mongodb://192.168.1.5:27017")
db = client["twStock"]
db.authenticate("twstock", "twstock123")
stockDay_coll = db['stockDay']
stockList = [{'x':10000, 'y':99999}
            ,{'x':5000,  'y':10000}
            ,{'x':2000,  'y':5000}
            ,{'x':1000,  'y':2000}
            ,{'x':0,     'y':1000}]
def runCom(v):
    codeList = stockDay_coll.find(
        {'date':'{:%Y%m%d}'.format(datetime.now() - timedelta(days=1))
        ,'Transaction':{'$gt':int(v['x']),'$lte':int(v['y'])}}
       ,{'_id':0, 'code':1, 'groupCode':1})
    return codeList

p = list( map(runCom, stockList))
stockCodeL = []
group = {}
for l in p:
    for st in l:
        stockCodeL.append(st['code']) #這次要查的股票們
        group[st['code']] = st['groupCode'] #用股票號碼回頭找group
    print(stockCodeL)
    stockCodeL = []

exit(0)
"""
stockList = ["01","02","20","03","21","12","04","18","14","28","05","22","06","08","09","10","11","15","25","24","31","27","26","29","39","23","16","17"]
#stockList = ["01"]
def runCom(L):
    return subprocess.Popen(cmd.format(L), shell=True)
p = list( map(runCom, stockList)) 
"""

def logW(L):
    return open("/python/log/stock{}.log".format(L.replace("|","_"),"a+"))
#fp = list( map(logW, stockList))

stop = len(stockList)

while stop > 0:
    for i in range(len(stockList)):
        #fp[i].write(p[i].stdout.readline())
        p[i].poll()
        logging.info(str(i) + " code(" + str(p[i].pid) + ")=" + str(p[i].returncode))
        if p[i].returncode == 0:
            stop = stop - 1
            p[i].kill
        elif p[i].returncode == None:
            #p[i].poll()
            None
        elif p[i].returncode != 0:
            p[i].kill
            p[i] = subprocess.Popen(cmd.format(stockList[i]), shell=True)
            
    time.sleep(10)
    logging.info(stop)
    """
    if stop == 0:
        for i in range(len(stockList)):
            fp[i].close()
    """        
