import pymongo
from datetime import timedelta, date, datetime
import sys
import time
import json
import os
import re
import logging

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s : %(message)s',
                    datefmt='%Y-%m-%dT %H:%M:%S',
                    filename='../../log/bak_{:%Y-%m-%d}.log'.format(datetime.now()))

bakComm = str(sys.argv[1])
type = str(sys.argv[2])
startDate = str(sys.argv[3])
#if len(sys.argv) >= 4:
endDate = str(sys.argv[4])
mode = False
if len(sys.argv) == 6:
    mode = bool(sys.argv[5])
filename = ""

if len(sys.argv) == 0:
    logging.error("======================================")
    logging.error("need give argv[1] bakComm{'bak','res'}")
    logging.error("          argv[2] type{'realtime','t86'}")
    logging.error("          argv[3] startDate{'YYYYMMDD'}")
    logging.error("          argv[4] endDate{'YYYYMMDD'}")
    logging.error("          argv[5] mode{1:test} not need")
    logging.error("  or give two argv for filename")
    sys.exit(0)

logging.error("======================================")
logging.error("argv[1] :" + bakComm)
logging.error("argv[2] :" + type)
logging.error("argv[3] :" + startDate)
logging.error("argv[4] :" + endDate)
if mode:
    logging.error("argv[5] :true")

if len(bakComm) == 0:
    sys.exit(0)
if len(type) == 0:
    sys.exit(0)
"""
if len(sys.argv) == 3:
    if bakComm == 'bak':
        print("filename not in bak")
        sys.exit(0)
    filename = str(sys.argv[2])
else:
"""
if len(startDate) == 0:
    sys.exit(0)
if len(endDate) == 0:
    sys.exit(0)

host = "172.18.0.2"
#host = "192.168.1.5"
port = "27017"
username = "twstock"
password = "twstock123"
dbname = "twStock"
collname = ""
bkcollname = ""
if type == 'realtime':
    collname = "realtime"
    bkcollname = "realtime_bak"
elif type == 't86':
    collname = "t86"
    bkcollname = "t86_bak"
outputs_dir = '../bak/'

client = pymongo.MongoClient("mongodb://"+host+":"+port)
db = client[dbname]
db.authenticate(username, password)
coll = db[collname]
collBak = db[bkcollname]

def daterange(start_date, end_date):
    if int ((end_date - start_date).days) == 0:
        yield start_date
    else:
        for n in range(int ((end_date - start_date).days) + 1 ):
            yield start_date + timedelta(n)

def render_output_locations(date_):
  return outputs_dir + date_ + "_" + collname + "_" + time.strftime("%Y%m%d_%H%M%S") + ".bak"

def run_backup(date_):
    jsonpath = render_output_locations(date_)
    with open(jsonpath, 'w') as f:
        for d in coll.find({'date':fdate},{'_id':0}):
            f.write(json.dumps(d) + "\n")

    f.close()

def collInsert(jsonList):
    if mode:
        collBak.insert_many(jsonList)
    else:
        coll.insert_many(jsonList)

def restore_file(file):
    try:
        jsonData = open(file, 'r')
        jsonList = []
        for line in jsonData:
            jsObj = json.loads(line)
            jsonList.append(jsObj)

            if len(jsonList) == 1000:
                logging.error("jsonList = 1000")
                collInsert(jsonList)
                jsonList = []
            """
            value = { "$set": jsObj }
            if "final_trade_volume" not in jsObj:
                query = {"code":jsObj.get('code'),"date":jsObj.get('date'),"accumulate_trade_volume":{"$gte":jsObj.get('accumulate_trade_volume')}}
            else:
                query = {"code":jsObj.get('code'),"date":jsObj.get('date'),"final_trade_volume":jsObj.get('final_trade_volume')}

            if mode:
                collRTBak.update_one(query, value, upsert=True)
            else:
                collRT.update_one(query, value, upsert=True)
            """
            #print(jsObj)
            #print(type(jsObj))
            #for key in jsObj.keys():
            #    print('key: %s  value: %s' % (key,jsObj.get(key)))

        if len(jsonList) != 0:
            logging.error("jsonList last")
            collInsert(jsonList)
            jsonList.clear

    except BaseException:
        logging.error(file + " load error ")
    else:
        jsonData.close()
        logging.error(file + " load success")

def run_restore(date_):
    if len(filename) > 0:
        restore_file(outputs_dir + filename)
    else:
        for f in os.listdir(outputs_dir):
            if re.search(date_ + "_" + type, f):
                if int(os.stat(outputs_dir + f).st_size) > 0:
                    logging.error(f)
                    query = {"date":date_}
                    if mode:
                        collBak.delete_many(query)
                    else:
                        coll.delete_many(query)
                    restore_file(outputs_dir + f)

if len(filename) > 0 :
    logging.error(filename)
    if bakComm == 'bak':
        run_backup(filename)
    elif bakComm == 'res':
        run_restore(filename)
    else:
        logging.error ('function error argv[1] need "bak" or "res"')
else:
    start_date = date(int(startDate[0:4]), int(startDate[4:6]), int(startDate[6:8]))
    end_date = date(int(endDate[0:4]), int(endDate[4:6]), int(endDate[6:8]))
    for date_ in daterange(start_date, end_date):
        fdate = date_.strftime("%Y%m%d")
        logging.error(fdate)
        if bakComm == 'bak':
            run_backup(fdate)
        elif bakComm == 'res':
            run_restore(fdate)
        else:
            logging.error('function error argv[1] need "bak" or "res"')
