import pymongo
myclient = pymongo.MongoClient("mongodb://172.17.0.3:27017")
print(myclient)
mydb = myclient["twStock"] 
mydb.authenticate("twstock", "twstock123")
dblist = myclient.list_database_names()
print(dblist)
collist = mydb.list_collection_names()
print(collist)
mycol = mydb["test"]
print(mycol)
mydict = { "name": "RUNOOB", "alexa": "10000", "url": "https://www.runoob.com" }
 
#x = mycol.insert_one(mydict) 
x = mycol.find_one()
print(x)

for x in mycol.find({},{ "_id": 0, "name": 1, "alexa": 1 }):
  print(x)
  
myquery = { "name": "RUNOOB" }
 
mydoc = mycol.find(myquery)
 
for x in mydoc:
  print(x)

print("gt")  
myquery = { "name": { "$gt": "H" } }
 
mydoc = mycol.find(myquery)
 
for x in mydoc:
  print(x)

print("regex")  
myquery = { "name": { "$regex": "^狗" } }
 
mydoc = mycol.find(myquery)
 
for x in mydoc:
  print(x)