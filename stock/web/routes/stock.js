const router = require('koa-router')();

// Router -> /
router.get('/kline', async(ctx) => {
    let code = ctx.request.query.code;
    await ctx.render('kline', {
        msg:'stock:' + code
    })
});

router.post('/KlineData', async(ctx) => {
    let code = ctx.request.body.code;
    console.log('code:'+code);
    if (code === undefined) code = '1101';

    ctx.response.type = 'json';
    let data = await ctx.db.collection('stockDay').aggregate([
        {
            $match:{
                $and:[
                    {code:{'$eq':code}}
                ]            
            }
        }, {
            $project:{
                '_id':0,
                'quoteTime':'$date',
                'preClose':'$Opening_Price',
                'open':'$Opening_Price',
                'high':'$Highest_Price',
                'low':'$Lowest_Price',
                'close':'$Closing_Price',
                'volume':'$Trade_Volume',
                'amount':'$Trade_Value'
           }
        }, {
            $sort:{
                'quoteTime':1
            }
        }
    ]).toArray();
    ctx.response.body = {'kline': data};
});

router.post('/TrendData', async(ctx) => {
    let code = ctx.request.body.code;
    let date = ctx.request.body.date;
    console.log('code:'+code+',date:'+date);
    if (code === undefined) code = '1101';
    if (date === undefined) date = '20200211';
    
    ctx.response.type = 'json';
    let data = await ctx.db.collection('realtime').aggregate([
        {
            $match:{
                $and:[
                    {code:{'$eq':code}
                   , date:{'$eq':date}
                    }
                ]
            }
        }, {
            $project:{
                '_id':0,
                //'code':1,
                //'date':1,
                'time':'$final_time',
                'price':'$latest_trade_price',
                'vol':'$trade_volume'
           }
        }, {
            $sort:{
                'time':1
            }
        }
    ]).toArray();
    let fdata = await ctx.db.collection('realtime').aggregate([
        {
            $match:{
                $and:[
                    {code:{'$eq':code}
                   , date:{'$eq':date}
                    }
                ]            
            }
        }, {
            $project:{
                '_id':0,
                'time':'09:00:00',
                'price':'$open',
                'vol':'0'
           }
        }, {$limit:1}
    ]).toArray();
    
    data.unshift(fdata[0]);
    
    ctx.response.body = data;
});

router.get('/KlineH', async(ctx) => {
    let code = ctx.request.query.code;
    await ctx.render('KlineH', {
        msg:'stock:' + code
    })
});

router.get('/Trend', async(ctx) => {
    let code = ctx.request.query.code;
    await ctx.render('Trend', {
        msg:'stock:' + code
    })
});

router.get('/crossline', async(ctx) => {
    let code = ctx.request.query.code;
    await ctx.render('crossline')
});

router.get('/js/painterKline.js', async(ctx) => {
    await ctx.render('js/painterKline')
});

router.get('/js/painterKlineH.js', async(ctx) => {
    await ctx.render('js/painterKlineH')
});

router.get('/js/painterTrend.js', async(ctx) => {
    await ctx.render('js/painterTrend')
});

router.get('/js/util.js', async(ctx) => {
    await ctx.render('js/util')
});

router.get('/js/absPainter.js', async(ctx) => {
    await ctx.render('js/absPainter')
});

router.get('/js/axis.js', async(ctx) => {
    await ctx.render('js/axis')
});

router.get('/js/axis-x.js', async(ctx) => {
    await ctx.render('js/axis-x')
});

router.get('/js/axis-y.js', async(ctx) => {
    await ctx.render('js/axis-y')
});

router.get('/js/k-line.js', async(ctx) => {
    await ctx.render('js/k-line')
});

router.get('/js/control.js', async(ctx) => {
    await ctx.render('js/control')
});

router.get('/js/controlbar.js', async(ctx) => {
    await ctx.render('js/controlbar')
});

router.get('/js/line.js', async(ctx) => {
    await ctx.render('js/line')
});

router.get('/js/cross.js', async(ctx) => {
    await ctx.render('js/cross')
});

router.get('/js/k-data.js', async(ctx) => {
    await ctx.render('js/k-data')
});

module.exports = router;