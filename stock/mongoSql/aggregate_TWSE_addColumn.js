db.getCollection('t86').aggregate([
    {
        $match:{
            $and:[
                {date:{'$gte':'20191101', '$lte':'20191122'}}
            ]
            
        }
    },
    {
        $lookup:{
            from:'TWSE',
            localField:'code',
            foreignField:'code',
            as:'codeinfo'}
    },
    {
        $unwind:'$codeinfo'
    },
    {
        $project:{
            'code':1,'DHedge_I':1,'groupCode':'$codeinfo.groupCode'
        }
    }
    /*,
    {
        $redact: {
            $cond: [
                {'$eq':['$codeinfo',[]]}
               ,"$$PRUNE","$$DESCEND"
            ]
        }
    },
    {
        $project:{
            'code':1,'DHedge_I':1,
            'codeinfo':{
                $filter:{
                    input:'$codeinfo',
                    as:'groupCode',
                    cond:{'$eq':['$$groupCode.groupCode','01']}
                }
            }
        }
    }
    */
])