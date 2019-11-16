import pymongo
from datetime import timedelta, date
import sys
import time
import json
import os
import re

bakComm = str(sys.argv[1])
startDate = str(sys.argv[2])
endDate = str(sys.argv[3])

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
    with open(jsonpath, 'w') as f:
        for d in collRT.find({'date':fdate},{'_id':0}):
            f.write(json.dumps(d) + "\n")
            
    f.close()
    
def run_restore(date_):
    for f in os.listdir(outputs_dir):
        if re.search(date_, f):
            print(f)
            if int(os.stat(outputs_dir + f).st_size) > 0:
                jsonData = open(outputs_dir + f)
                #try:
                jsObj = json.load(jsonData)
                print(jsObj)
                print(type(jsObj)) 
                for key in jsObj.keys(): 
                    print('key: %s  value: %s' % (key,jsObj.get(key))) 
                #except BaseException:
                #    print(f + " load error ")
                #else:
                jsonData.close()
                #    print(f + " load success")
    
start_date = date(int(startDate[0:4]), int(startDate[5:6]), int(startDate[6:8]))
end_date = date(int(endDate[0:4]), int(endDate[5:6]), int(endDate[6:8]))
for date_ in daterange(start_date, end_date):
    fdate = date_.strftime("%Y%m%d")
    print(fdate)
    if bakComm == 'bak':
        run_backup(fdate)
    elif bakComm == 'res':
        run_restore(fdate)
    else:
        print ('function error argv[1] need "bak" or "res"')
    