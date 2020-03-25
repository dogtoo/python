#!/usr/bin/python
import pymongo
import time
from datetime import timedelta, date, datetime
import os
import logging
import json
import configparser
config = configparser.ConfigParser()
config.read("../config.ini")

import threading

from stock2 import get

debug = False

if config['stock']['logginglevel'] == 'DEBUG':
    level = logging.DEBUG
    debug = True
elif config['stock']['logginglevel'] == 'INFO':
    level = logging.INFO
elif config['stock']['logginglevel'] == 'ERROR':
    level = logging.ERROR

logging.basicConfig(level=level,
                    format='%(asctime)s - %(levelname)s : %(message)s',
                    datefmt='%Y-%m-%dT %H:%M:%S',
                    filename=config['stock']['logfilelink'] + 'realTimeRun2' + '_' + '{:%Y-%m-%d}'.format(datetime.now()) + '.log' )

client = pymongo.MongoClient(config['stock']['dbConn'])
db = client["twStock"]
db.authenticate(config['stock']['dbuser'],config['stock']['dbpass'])

collRL = db['realTimeLine']

r = collRL.aggregate([
    {'$group':{'_id':'$group'}},
    {'$sort':{'_id':1}},
    {'$project':{'_id':0,'group':'$_id'}}
])
runnum = []
for r_ in r:
    runnum.append(r_['group'])

realTimeLine = {}
runtime = 0

def chkRun():
    sysTime = int( '{:%d%H%M}'.format(datetime.now()) )
    # 9:00 起
    strTime = int( '{:%d}'.format(datetime.now()) + '0859' )
    # 13:40 結束
    endTime = int( '{:%d}'.format(datetime.now()) + '1340' )
    # 15:00 零股結算
    secBTime = int( '{:%d}'.format(datetime.now()) + '1459' )
    secETime = int( '{:%d}'.format(datetime.now()) + '1510' )
    logging.debug("sysTime = " + str(sysTime) + ", strTime = " + str(strTime) + ", endTime = " + str(endTime) + ", secBTime = " + str(secBTime) + ", secETime = " + str(secETime))
    if sysTime > strTime and sysTime < endTime:
        return True
    elif sysTime > secBTime and sysTime < secETime:
        return True
    else:
        return False

threads = []
while True:
    for r_ in runnum:
        g = 'G'+str(r_)
        
        if g not in realTimeLine:
            realTimeLine[g] = {}
            groupData = collRL.find({'group':r_},{'_id':0,'code':1,'line':1})
            realTimeLine[g]['code'] = []
            realTimeLine[g]['line'] = []
            for gd_ in groupData:
                realTimeLine[g]['code'].append(gd_['code'])
                realTimeLine[g]['line'].append(gd_['line'])
            realTimeLine[g]['run'] = 1
            
        logging.info('Line:' + g)
        run = realTimeLine[g]['run'] - 1
        logging.info('    run Group Line: ' + realTimeLine[g]['line'][run])
        scg = realTimeLine[g]['code'][run]
        stop = True
        try:
            #get(scg, g, db, logging, debug)
            if len(threads) < r_ or not threads[(r_-1)].isAlive():
                logging.info('    Start Thread:' + g)
                if len(threads) < r_:
                    threads.append(threading.Thread(target = get, args = (scg, g, db, logging, debug)))
                else:
                    threads[(r_-1)] = threading.Thread(target = get, args = (scg, g, db, logging, debug))
                threads[(r_-1)].start()
                stop = False
            else:
                logging.info('    ' + g + ' Thread is run:')
        except BaseException as e:
            logging.error("    get stock fall :" + str(e))        
        
        if not stop:
            run = run+1
            logging.debug('    line = ' + str(len(realTimeLine[g]['line'])) + ', ' + str(run))
            if len(realTimeLine[g]['line']) == run:
                run = 1
            else:
                run = run + 1
            realTimeLine[g]['run'] = run
            logging.debug('    next run ' + str(run))
    
    #for i in range(r_):
    #    threads[i].join()
    
    time.sleep(1)
    if debug:
        runtime = runtime + 1
        if runtime == 500:
            break
    elif not chkRun():
        logging.info('stock close')
        break
        
