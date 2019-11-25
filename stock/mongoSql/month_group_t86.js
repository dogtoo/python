db.getCollection('t86').aggregate([
    {
        $match:{
            $and:[
                {date:{'$gte':'20190101', '$lte':'20191131'}}
               //,{groupCode:{'$eq':'03'}}
               ,{groupCode:{'$ne':'00'}}
            ]
        }
    },
    {
        $group:{
            _id: {
                date:{$substr:['$date', 0, 4]}
              , groupCode:'$groupCode'
               // , code:'$code'
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
        $project: {
            date: '$_id.date'
           ,groupCode: '$_id.groupCode'
           ,'外資買進':{$divide:['$FII_I', 10000]}
           ,'外資賣出':{$divide:['$FII_O', 10000]}
           ,'外資增減':{$subtract:['$FII_I', '$FII_O']}
           ,'投信買進':{$divide:['$SIT_I', 10000]}
           ,'投信賣出':{$divide:['$SIT_O', 10000]}
           ,'投信增減':{$subtract:['$SIT_I', '$SIT_O']}
           ,'自營商買進':{$divide:['$DProp_I', 10000]}
           ,'自營商賣出':{$divide:['$DProp_O', 10000]}
           ,'自營商買進避':{$divide:['$DHedge_I', 10000]}
           ,'自營商賣出避':{$divide:['$DHedge_O', 10000]}
        }
    },
    {
        $sort:{
            '外資增減':-1
        }
    }
])