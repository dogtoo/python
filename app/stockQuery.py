#!/usr/bin/python
import pprint
import pymongo
import time
import sys

stockGroupCode = sys.argv[1]
runGroupStr = sys.argv[2]
runGroupSet = set(runGroupStr.split(","))
if stockGroupCode not in runGroupSet:
    print("input code:", stockGroupCode, " not in " + runGroupStr)
else:
    print("input code:", stockGroupCode, " in " + runGroupStr)


client = pymongo.MongoClient("mongodb://172.17.0.3:27017")
db = client["twStock"]
db.authenticate("twstock", "twstock123")

t = (2018, 12, 28, 8, 44, 4, 4, 362, 0)

"""
coll = db["realtime"]
query = {"code":"2330"}
doc = coll.find(query)
print(type(doc))
for x in doc:
    print(type(x))
    print(x)
"""

coll = db["TWSE"]
doc = coll.find({'groupCode':{'$regex':stockGroupCode}}, {"_id": 0, "code":1, "groupCode":1})
"""
match = {
	'groupCode': '24'
}
groupby = 'code'
group = {
	'_id': "$%s" % (groupby if groupby else None)
}
doc = coll.aggregate(
	[
		{'$match': match},
		{'$group': group},
	]
)
"""
t=0
s=15
i=1
for x in doc:
    t = t + 1
    print(x['code'])
    print(x['groupCode']+"_"+str(i))
    query = {"code":x['code']}
    value = { "$set": {'groupCode': x['groupCode']+"_"+str(i)} }
    coll.update_one(query, value, upsert=True)
    
    if t == s:
        t = 0
        i = i + 1
    
    #for code,data in x.items():
    #    pprint.pprint(data)
    """
    if k == '半導體業':
        print(len(data))
        t = len(data)
        spl = 5
        for code,v in data.items():
            pprint.pprint(code)
    """
