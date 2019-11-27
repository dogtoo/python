var t86CodeByDate =
db.getCollection('t86').aggregate([
    {
        $match:{
            $and:[
                {date:{'$gte':'20190601', '$lte':'20191131'}}
               //,{groupCode:{'$eq':'03'}}
               //,{groupCode:{'$ne':'00'}}
                ,{code:{$eq:'2323'}}
            ]
        }
    },
    {
        $group:{
            _id: {
                date:{$substr:['$date', 0, 8]}
              //, groupCode:'$groupCode'
                , code:'$code'
            }
           ,'FII_I':{$sum:'$FII_I'}
           ,'FII_O':{$sum:'$FII_O'}
           ,'SIT_I':{$sum:'$SIT_I'}
           ,'SIT_O':{$sum:'$SIT_O'}
           ,'DProp_I':{$sum:'$DProp_I'}
           ,'DProp_O':{$sum:'$DProp_O'}
           ,'DHedge_I':{$sum:'$DHedge_I'}
           ,'DHedge_O':{$sum:'$DHedge_O'}
        }
    },
    {
        $sort:{
            '_id':1
        }
    },
    {
        $lookup:{
            from: 'TWSE',
            localField:'_id.code',
            foreignField:'code',
            as:'codeinfo'
        }
    },
    {
        $unwind:'$codeinfo'
    },
    {
        $project: {
            _id: 0
           ,date: '$_id.date'
           ,code: '$_id.code'
           ,name: '$codeinfo.name'
           ,'�~��R�i':{$divide:['$FII_I', 10000]}
           ,'�~���X':{$divide:['$FII_O', 10000]}
           ,'�~��W��':{$divide:[{$subtract:['$FII_I', '$FII_O']}, 10000]}
           ,'��H�R�i':{$divide:['$SIT_I', 10000]}
           ,'��H��X':{$divide:['$SIT_O', 10000]}
           ,'��H�W��':{$divide:[{$subtract:['$SIT_I', '$SIT_O']}, 10000]}
           ,'����ӶR�i':{$divide:['$DProp_I',10000]}
           ,'����ӽ�X':{$divide:['$DProp_O', 10000]}
           ,'����ӶR�i��':{$divide:['$DHedge_I', 10000]}
           ,'����ӽ�X��':{$divide:['$DHedge_O', 10000]}
        }
    }
])
var acc = 0
t86CodeByDate.forEach(function(item, index, array) {
    acc = acc + item.�~��W��
    print(item.date+','+ item.�~��R�i+','+item.�~���X+','+item.�~��W��+','+acc)
    //print(item)
});