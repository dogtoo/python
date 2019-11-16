import pymongo
from datetime import timedelta, date
import sys
import time
#import os
from bson.json_util import dumps
import json

startDate = str(sys.argv[1])
endDate = str(sys.argv[2])

host = "172.18.0.2"
port = "27017"
username = "twstock"
password = "twstock123"
dbname = "twStock"
collname = "realtime"
bkcollname = "realtime_bak"
outputs_dir = '/python/stock/bak/'

client = pymongo.MongoClient("mongodb://"+host+":"+port)
db = client[dbname]
db.authenticate(username, password)
collRT = db[collname]
collRTBak = db[bkcollname]

def daterange(start_date, end_date):
    if int ((end_date - start_date).days) == 0:
        yield start_date
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def render_output_locations(date_):
  return outputs_dir + date_ + "_" + time.strftime("%d-%m-%Y-%H:%M:%S") + ".bak"

def run_backup(date_):
    
    jsonpath = render_output_locations(date_)
    with open(jsonpath, 'wb') as jsonfile:
        for d in collRT.find({'date':fdate}):
        jsonfile.write(d)

start_date = date(int(startDate[0:4]), int(startDate[5:6]), int(startDate[6:8]))
end_date = date(int(endDate[0:4]), int(endDate[5:6]), int(endDate[6:8]))
for date_ in daterange(start_date, end_date):
    fdate = date_.strftime("%Y%m%d")
    print(fdate)
    #collRTBak.insert_many( collRT.find({'date':fdate}))
    run_backup(fdate)
    collRTBak.delete_many({})