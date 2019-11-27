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
           ,'外資買進':{$divide:['$FII_I', 10000]}
           ,'外資賣出':{$divide:['$FII_O', 10000]}
           ,'外資增減':{$divide:[{$subtract:['$FII_I', '$FII_O']}, 10000]}
           ,'投信買進':{$divide:['$SIT_I', 10000]}
           ,'投信賣出':{$divide:['$SIT_O', 10000]}
           ,'投信增減':{$divide:[{$subtract:['$SIT_I', '$SIT_O']}, 10000]}
           ,'自營商買進':{$divide:['$DProp_I',10000]}
           ,'自營商賣出':{$divide:['$DProp_O', 10000]}
           ,'自營商買進避':{$divide:['$DHedge_I', 10000]}
           ,'自營商賣出避':{$divide:['$DHedge_O', 10000]}
        }
    }
])
var acc = 0
t86CodeByDate.forEach(function(item, index, array) {
    acc = acc + item.外資增減
    print(item.date+','+ item.外資買進+','+item.外資賣出+','+item.外資增減+','+acc)
    //print(item)
});