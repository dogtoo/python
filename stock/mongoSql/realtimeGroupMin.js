db.getCollection('realtime').aggregate([
{
    $match:{
        $and:[
            {'date':'20200327'},{'code':'2105'}
        ]
    }
},
{
    $sort:{'timestamp':-1}
},
{
    $project:{
        'time':'$final_time',
        'hour':{ $hour: {$convert:{'input':{$concat:['2020-03-27','T','$final_time']},'to':'date'}}},
        'min':{ $minute: {$convert:{'input':{$concat:['2020-03-27','T','$final_time']},'to':'date'}}},
        'acc_tv':'$accumulate_trade_volume',
        'latest_trade_price':'$latest_trade_price',
        'trade_volume':'$trade_volume',
        'best_bid_price':{$arrayElemAt:['$best_bid_price',0]}
        //min: {$minute:{new Date('$date'+'T'+'$final_time')}}
    }
},
{
    $group:{
        _id: {
            hour:'$hour',
            min:'$min'
        },
        'acc_tv_max':{$max:'$acc_tv'},
        'acc_tv_min':{$min:'$acc_tv'},
        'latest_trade_price':{$last:'$latest_trade_price'},
        'best_bid_price':{$last:'$best_bid_price'},
        'trade_volume':{$first:'$trade_volume'},
        'trade_volume_l':{$last:'$trade_volume'}
    }
},
{
    $sort:{'_id.hour':1,'_id.min':1}
}
])