db.getCollection('t86').aggregate([
    {
        $match:{
            $and:[
                {date:{'$gte':'20190101', '$lte':'20191131'}}
               ,{groupCode:{'$eq':'28'}}
               //,{groupCode:{'$ne':'00'}}
            ]
        }
    },
    {
        $group:{
            _id: {
                date:{$substr:['$date', 0, 4]}
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
            date: '$_id.date'
           ,code: '$_id.code'
           ,namd: '$codeinfo.name'
           ,'�~��R�i':{$divide:['$FII_I', 10000]}
           ,'�~���X':{$divide:['$FII_O', 10000]}
           ,'�~��W��':{$subtract:['$FII_I', '$FII_O']}
           ,'��H�R�i':{$divide:['$SIT_I', 10000]}
           ,'��H��X':{$divide:['$SIT_O', 10000]}
           ,'��H�W��':{$subtract:['$SIT_I', '$SIT_O']}
           ,'����ӶR�i':{$divide:['$DProp_I', 10000]}
           ,'����ӽ�X':{$divide:['$DProp_O', 10000]}
           ,'����ӶR�i��':{$divide:['$DHedge_I', 10000]}
           ,'����ӽ�X��':{$divide:['$DHedge_O', 10000]}
        }
    },
    {
        $sort:{
            '�~��W��':-1
        }
    }
])