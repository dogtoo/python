#!/usr/bin/python
#test: {'scl':['1316','1708'],'scg':{'1316':'21','1708':'21'},'level':'A1'} false
import twstock
import pymongo
import sys
import logging
import requests

from datetime import timedelta, date, datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

import json
import configparser
config = configparser.ConfigParser()
config.read("../config.ini")

class SSLContextAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        kwargs['ssl_context'] = context
        context.load_default_certs() # this loads the OS defaults on Windows
        return super(SSLContextAdapter, self).init_poolmanager(*args, **kwargs)

def get(scg, level, db, logging, debug):
    
    collname = ""
    if debug:
        collname = "realtime_"
    else:
        collname = "realtime"
    collRT = db[collname]

    try:
        SESSION_URL = config['stock']['url']
        req = requests.Session()
        adapter = SSLContextAdapter()
        req.mount(SESSION_URL, adapter)
        #res = req.get(SESSION_URL, timeout=(5, 5), verify=True)
        scl = list(scg.keys())
        stock = twstock.realtime.get(scl, req, {}, logging)
        if stock["success"]:
            logging.info("    get success:" + str(len(stock)))
            #轉換格式
            for code, v in stock.items():
                logging.debug(str(code) + ' ' + str(v))
                if isinstance(v, dict) and v['success']:
                    try:
                        del v['info']
                        rlTime = v['realtime']
                        del v['realtime']
                        v.update(rlTime)
                        v.update({'group':scg[code]})
                        #存入db
                        #新的訊息有可能沒有交易，新增一筆的方式是要張數有增加
                        query = {"code":v['code'],"date":v['date'],"accumulate_trade_volume":{"$gte":v['accumulate_trade_volume']}}
                        value = { "$set": v}
                        #l = collRT.find({"code":v['code'],"date":v['date']}).sort('final_time', 1).limit(1)
                        #logging.debug("    last:" + str(l[0]))
                        
                        if "final_trade_volume" not in v:
                            logging.debug("    " + str({"accumulate_trade_volume":v['accumulate_trade_volume'] , "trade_volume":v['trade_volume']} ))
                            if v['trade_volume'] > v['accumulate_trade_volume']:
                                logging.error("    t_v > a_t_v : " + str(v))
                                #lquery = {"code":v['code'],"date":v['date']}
                                #l = collRT.find(lquery).sort({'final_time':1}).limit(1)
                            collRT.update_one(query, value, upsert=True)
                        else:
                            query = {"code":v['code'],"date":v['date'],"final_trade_volume":v['final_trade_volume']}
                            logging.debug("    " + str({"final_trade_volume":v['final_trade_volume'] , "trade_volume":v['trade_volume']}))
                            value = {"$set":v}
                            collRT.update_one(query, value, upsert=True)
                    except BaseException as e:
                        logging.error("    BaseException :" + str(e))
                else:
                    if str(code) != 'success':
                        logging.error("    code :" + str(code) + " get false " + str(v))
        else:
            logging.error("    get error:" + str(len(scl)))
            logging.error("    get error:" + stock['rtmessage'])
        
    except BaseException as e:
        logging.error("stock fal :" + str(e))
        
    

if __name__ == '__main__':
    args_ = sys.argv[1]
    debug = sys.argv[2]
    #print(type(args_))
    args = json.loads(args_.replace("'", "\""))
    #print(len(args['scl']))
    if 'level' not in args:
        sys.exit(0)
    stockCodeLevel = args['level']
    #if 'scl' not in args:
    #    sys.exit(0)
    #stockCodeList = args['scl']
    if 'scg' not in args:
        sys.exit(0)
    stockCodeGroup = args['scg']

    if config['stock']['logginglevel'] == 'DEBUG':
        level = logging.DEBUG
    elif config['stock']['logginglevel'] == 'INFO':
        level = logging.INFO
    elif config['stock']['logginglevel'] == 'ERROR':
        level = logging.ERROR

    logging.basicConfig(level=level,
                        format='%(asctime)s - %(levelname)s : %(message)s',
                        datefmt='%Y-%m-%dT %H:%M:%S',
                        filename=config['stock']['logfilelink'] + stockCodeLevel + '_' + '{:%Y-%m-%d}'.format(datetime.now()) + '.log' )

    client = pymongo.MongoClient(config['stock']['dbConn'])
    db = client["twStock"]
    db.authenticate(config['stock']['dbuser'],config['stock']['dbpass'])
    
    get(stockCodeGroup, stockCodeLevel, db, logging, debug)
    sys.exit(0)
    