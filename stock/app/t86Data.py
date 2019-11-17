#!/usr/bin/python
import twstock
import pymongo
import time
import sys
#import pandas as pd

bDate = sys.argv[1]
eDate = sys.argv[2]
groupCode=""
if len(sys.argv) >= 3:
    groupCode = sys.argv[3]
group = []

client = pymongo.MongoClient("mongodb://172.18.0.2:27017")
db = client["twStock"]
db.authenticate("twstock", "twstock123")
collRT = db["TWSE"]
collT86 = db["t86"]

def daterange(start_date, end_date):
    if int ((end_date - start_date).days) == 0:
        yield start_date
    else:
        for n in range(int ((end_date - start_date).days) + 1 ):
            yield start_date + timedelta(n)

if groupCode:
    group = [groupCode]
else:
    #抓群組代碼
    group = collRT.distinct('groupCode')
print(group)
#bDate = '20190601'
#eDate = '20190630'
#datelist = pd.bdate_range(bDate, eDate).strftime("%Y%m%d")
#for date in datelist:
start_date = date(int(bDate[0:4]), int(bDate[4:6]), int(bDate[6:8]))
end_date = date(int(eDate[0:4]), int(eDate[4:6]), int(eDate[6:8]))
for date in daterange(start_date, end_date):
    print(date)
    for code in group:
        print("  " + code)
        r = twstock.t86.get(code, date, 'json')
        if 'data' in r:
            data = r['data']
            for h in data:
                query = {"code":h['code'],"date":h['date']}
                value = { "$set": h }
                collT86.update_one(query, value, upsert=True)
            time.sleep(30)
        else:
            print(r)
        
        