#!/usr/bin/python
import twstock
import pymongo
import time
import sys

bDate = sys.argv[1]
eDate = sys.argv[2]
groupCode = sys.argv[3]
group = []

client = pymongo.MongoClient("mongodb://172.17.0.3:27017")
db = client["twStock"]
db.authenticate("twstock", "twstock123")
collRT = db["TWSE"]

if groupCode:
    group[0] = groupCode
else:
    #抓群組代碼
    group = collRT.distinct('groupCode')
    
for date in bDate .. eDate
    print date
#data = twstock.t86.get('01', '20190620', 'json')