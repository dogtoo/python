var t = db.getCollection('TWSE').find({})
t.forEach(function(item, index, array) {
    db.getCollection('t86').update(
        {'code':item.code}
       ,{'$set':{'groupCode':item.groupCode}}
       ,{multi:true}
    )
});