db.getCollection('realtime').aggregate([
    {
        $match:{
            $and:[
                {code:{'$eq':'2002'}
               , date:{'$eq':'20200206'}
                }
            ]            
        }
    }, {
        $project:{
            '_id':0,
            'code':1,
            'date':1,
            'time':'$final_time',
            'price':'$latest_trade_price',
            'vol':'$trade_volume'
       }
    }, {
        $sort:{
            'time':1
        }
    }
])