db.getCollection('t86').aggregate([
    {
        $match:{
            date:{$gte:'20190501',$lte:'20190531'}
        }
    },
    {
        $group:{
            _id:'$date'
           ,count:{$sum:1}
        }
    },
    { $project : {
        _id : 1 ,
        count : 1 ,
    }},
    {
        $sort:{_id:1}
    }
])