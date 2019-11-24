db.getCollection('t86').aggregate([
    {
        $match:{
            $and:[
                {date:{'$gte':'20190101', '$lte':'20191122'}}
            ]
            
        }
    },
    {
        $group:{
            _id:'$groupCode'
           ,totalSaleAmount: { 
               $sum: { 
                   $multiply: [ $DHedge_I, "$DHedge_O" ] 
               } 
            }
 
        }
    }
])