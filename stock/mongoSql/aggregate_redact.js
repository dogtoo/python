db.getCollection('t86').aggregate([
    {
        $match:{
            $and:[
                {date:{'$gte':'20191101', '$lte':'20191122'}}
               ,{$or: [
                {code:'2105'}
                ,{code:'1101'}]}
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
        $project:{
            'code':1,'DHedge_I':1,'codeinfo':1
        }
    },
    {
        $redact: {
            $cond: [
                {'$eq':['$$codeinfo.groupCode','01']}
               ,"$$DESCEND"
               , "$$PRUNE"
            ]
        }
    }
])