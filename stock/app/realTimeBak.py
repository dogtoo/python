import pymongo
from datetime import timedelta, date
import sys

startDate = str(sys.argv[1])
endDate = str(sys.argv[2])
client = pymongo.MongoClient("mongodb://172.18.0.2:27017")
db = client["twStock"]
db.authenticate("twstock", "twstock123")
collRT = db["realtime"]
collRTBak = db["realtime_bak"]

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(startDate[0:4], startDate[5:6], startDate[6:8])
end_date = date(endDate[0:4], endDate[5:6], endDate[6:8])
for date_ in daterange(start_date, end_date):
    print(date_.strftime("%Y%m%d"))
    quryRT = collRTBak.insertMany( collSt.find({'date':date_.strftime("%Y%m%d")}).toArray())
    