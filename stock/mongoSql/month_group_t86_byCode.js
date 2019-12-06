var t86CodeByDate =
db.getCollection('t86').aggregate([
    {
        $match:{
            $and:[
                {date:{'$gte':'20190601', '$lte':'20191231'}}
               //,{groupCode:{'$eq':'03'}}
               //,{groupCode:{'$ne':'00'}}
                ,{code:{$eq:'2328'}}
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
           ,'外資買進':{$divide:['$FII_I', 1000]}
           ,'外資賣出':{$divide:['$FII_O', 1000]}
           ,'外資增減':{$divide:[{$subtract:['$FII_I', '$FII_O']}, 1000]}
           ,'投信買進':{$divide:['$SIT_I', 1000]}
           ,'投信賣出':{$divide:['$SIT_O', 1000]}
           ,'投信增減':{$divide:[{$subtract:['$SIT_I', '$SIT_O']}, 1000]}
           ,'自營商買進':{$divide:['$DProp_I',1000]}
           ,'自營商賣出':{$divide:['$DProp_O', 1000]}
           ,'自營商買進避':{$divide:['$DHedge_I', 1000]}
           ,'自營商賣出避':{$divide:['$DHedge_O', 1000]}
           ,'累計股數':{$convert:{
                        input:'0'
                       ,to: 'int'}}
        }
    },
    {
        $lookup:{
            from: 'stockDay',
            let:{
                stockCode:'$code'
               ,stockDate:'$date'
            },
            pipeline: [
                {
                    $match:{
                        $expr:{
                            $and: [
                                {$eq:['$code', '$$stockCode']}
                               ,{$eq:['$date', '$$stockDate']}
                            ]
                        }
                    }
                }
            ],
            as:'stockDay'
        }
    },
    {
        $unwind:'$stockDay'
    },
    {
        $project: {
            _id: 0
           ,date: 1
           ,code: 1
           ,name: 1
           ,'外資買進':1
           ,'外資賣出':1
           ,'外資增減':1
           ,'投信買進':1
           ,'投信賣出':1
           ,'投信增減':1
           ,'自營商買進':1
           ,'自營商賣出':1
           ,'自營商買進避':1
           ,'自營商賣出避':1
           ,'累計股數':1
           ,'Closing_Price':'$stockDay.Closing_Price'
        }
    }
])
var acc = 0
t86CodeByDate.forEach(function(item, index, array) {
    acc = acc + item.外資增減;
    //print(item.date+','+ item.外資買進+','+item.外資賣出+','+item.外資增減+','+acc)
    item.累計股數 = acc;
    print(item)
});

