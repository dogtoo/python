db.getCollection('t86').aggregate([
    {
        $match:{
            $and:[
                {date:{'$gte':'20190401', '$lte':'20191131'}}
               ,{groupCode:{'$eq':'01'}}
            ]
        }
    },
    {
        $group:{
            _id: {
                date:{$substr:['$date', 0, 6]}
              , groupCode:'$groupCode'
            }
           ,'外資買進':{$sum:'$FII_I'}
           ,'外資賣出':{$sum:'$FII_O'}
           ,'投信買進':{$sum:'$SIT_I'}
           ,'投信賣出':{$sum:'$SIT_O'}
           ,'自營商買進':{$sum:'$DProp_I'}
           ,'自營商賣出':{$sum:'$DProp_O'}
           ,'自營商買進避':{$sum:'$DHedge_I'}
           ,'自營商賣出避':{$sum:'$DHedge_O'}
        }
    },
    {
        $sort:{
            '_id':1
        }
    }
])