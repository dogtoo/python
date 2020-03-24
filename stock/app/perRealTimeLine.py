#!/usr/bin/python
import twstock
import pymongo
import sys
import logging
import re

from datetime import timedelta, date, datetime

import json
import configparser
config = configparser.ConfigParser()
config.read("../config.ini")

if config['stock']['logginglevel'] == 'DEBUG':
    level = logging.DEBUG
elif config['stock']['logginglevel'] == 'INFO':
    level = logging.INFO
elif config['stock']['logginglevel'] == 'ERROR':
    level = logging.ERROR

logging.basicConfig(level=level,
                    format='%(asctime)s - %(levelname)s : %(message)s',
                    datefmt='%Y-%m-%dT %H:%M:%S',
                    filename=config['stock']['logfilelink'] + 'perRealTimeLine' + '_' + '{:%Y-%m-%d}'.format(datetime.now()) + '.log' )
                    
client = pymongo.MongoClient(config['stock']['dbConn'])
db = client["twStock"]
db.authenticate(config['stock']['dbuser'],config['stock']['dbpass'])

collSD = db['stockDay']
collRL = db['realTimeLine']
                    
now = '{:%Y%m%d}'.format(datetime.now())
date_ = collSD.find({'date':{'$lt':now}},{'_id':0,'date':1}).sort('date',-1).limit(1)[0]['date']
logging.debug('date:'+str(date_))
q1 = {'date': date_
     ,'$or':[
           {'groupCode':{'$ne':'00'}}
          ,{'groupCode':{'$eq':'00'}, 'Transaction':{'$gt':100}}
      ]
     ,'Transaction':{'$gt':0}
}
q2 = {'date': date_
     ,'$or':[
           {'groupCode':{'$eq':'00'}, 'Transaction':{'$lte':100}}
          ,{'groupCode':{'$ne':'00'}, 'Transaction':{'$eq':0}}
      ]
}
sp = [{}]
max = config['rtgroup']['Max']
idx = 0
logging.debug('Max:'+str(max))
stock = collSD.find(q1, {'_id':0, 'code':1, 'groupCode':1}).sort('Transaction',-1);
urlLen_ = 0
for code in stock:
    urlLen_ = urlLen_ + len(code['code']) + 8
    if len(sp[idx]) == int(max) or urlLen_ > 2000:
        idx = idx + 1
        sp.append({})
        urlLen_ = 0
    sp[idx][code['code']] = code['groupCode']
    
stock = collSD.find(q2, {'_id':0, 'code':1, 'groupCode':1}).sort('Transaction',-1);
for code in stock:
    urlLen_ = urlLen_ + len(code['code']) + 8
    if len(sp[idx]) == int(max) or urlLen_ > 1900:
        idx = idx + 1
        sp.append({})
        urlLen_ = 0
    sp[idx][code['code']] = code['groupCode']
    
logging.debug('perLine:' + str(len(sp)))
for lineCode in sp:
    logging.debug(str(lineCode))

gcount = 0
collRL.delete_many({})
for g in range(6):
    group = config['rtgroup']['G'+str(g+1)]
    print(group)
    run = '*'
    re_group = re.search("^(\d*\w{1})(.*)", group)
    groupCode = re_group.group(1)
    r_ = re.split("-", re_group.group(2))
    if len(r_) == 1:
        value = {"$set": {'line': groupCode, 'code':sp[gcount], 'run':run, 'group':(g+1)}}
        logging.debug(value)
        collRL.update_one({'line': groupCode}, value, upsert=True)
        gcount = gcount + 1
    else:
        for r in range(int(r_[0]),int(r_[1])+1):
            groupCode_ = groupCode + str(r)
            value = {"$set": {'line': groupCode_, 'code':sp[gcount], 'run':run, 'group':(g+1)}}
            logging.debug(value)
            collRL.update_one({'line': groupCode_}, value, upsert=True)
            run = ''
            gcount = gcount + 1
            if len(sp) == gcount:
                break