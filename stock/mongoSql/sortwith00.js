var data_ = db.getCollection('stockDay').find({'date':'20200323',$or:[
                    {groupCode:{'$ne':'00'}}
                    ,{groupCode:{'$eq':'00'}, Transaction:{$gt:100}}
                 ],'Transaction':{$gt:0}}, {_id:0, code:1, Transaction:1}).sort({Transaction:-1});
var T10 = 0;
var T5 = 0;
var T1 = 0;
var H5 = 0;
var H1 = 0;
var HD1 = 0;

data_.forEach(function(item, index, array) {
 //print(item.code+'¡A{Transaction:{$gt:0}} item.Transaction)
    if (item.Transaction > 10000)
        T10 = T10 + 1;
    else if (item.Transaction > 5000)
        T5++;
    else if (item.Transaction > 1000)
        T1++;
    else if (item.Transaction > 500)
        H5++;
    else if (item.Transaction > 100)
        H1++;
    else
        HD1++;
});
print('10T=' + T10 + ',5T=' + T5 + ',1T=' + T1 + ',5H=' + H5 + ',1H=' + H1 + ',1HD=' + HD1 );