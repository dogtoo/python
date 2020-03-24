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

from stock2 import get

if config['stock']['logginglevel'] == 'DEBUG':
    level = logging.DEBUG
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
#for r_ in r:
#    logging.debug(str(r_['group']))

realTimeLine = {}

while True:
    for r_ in r:
        g = 'G'+str(r_['group'])
        try:
            if g not in realTimeLine:
                realTimeLine[g] = {}
                groupData = collRL.find({'group':r_['group']},{'_id':0,'code':1,'line':1})
                realTimeLine[g]['code'] = []
                realTimeLine[g]['line'] = []
                for gd_ in groupData:
                    realTimeLine[g]['code'].append(gd_['code'])
                    realTimeLine[g]['line'].append(gd_['line'])
                realTimeLine[g]['run'] = 1
                
            logging.debug('Line:' + g)
            run = realTimeLine[g]['run'] - 1
            logging.debug('    run Group Line: ' + realTimeLine[g]['line'][run])
            scg = realTimeLine[g]['code'][run]
            get(scg, g, db, logging, 'true')
            run = run+1
            if len(realTimeLine[g]['line']) == run:
                run = 1
            else
                run = run + 1
            realTimeLine[g]['run'] = run
        except BaseException as e:
            logging.error("proxy fal :" + str(e))
    #time.sleep(3)
    break
