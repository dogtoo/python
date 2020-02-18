const router = require('koa-router')();
const dateFormat = require('dateformat');
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
    
    var year = new Date();
    year.setFullYear(year.getFullYear() - 2);
    var year_ = dateFormat(year, 'yyyymmdd');
    
    ctx.response.type = 'json';
    let data = await ctx.db.collection('stockDay').aggregate([
        {
            $match:{
                $and:[
                    {code:{'$eq':code}}
                   ,{date:{'$gte':year_}}
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
    var date = new Date();
    var date_ = dateFormat(date, 'yyyymmdd');
    console.log('code:'+code+',date:'+date_);
    if (code === undefined) code = '1101';
    if (date_ === undefined) date_ = '20200211';
    
    ctx.response.type = 'json';
    let data = await ctx.db.collection('realtime').aggregate([
        {
            $match:{
                $and:[
                    {code:{'$eq':code}
                   , date:{'$eq':date_}
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
    
    if (parseInt(data[0].time.substr(1, 2)) < 9) {
        data.shift();
    }
    
    let fdata = await ctx.db.collection('realtime').aggregate([
        {
            $match:{
                $and:[
                    {code:{'$eq':code}
                   , date:{'$eq':date_}
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

router.get('/Trend', async(ctx) => {
    let code = ctx.request.query.code;
    await ctx.render('Trend', {
        msg:'stock:' + code
    })
});

//取得上月外資可用資金
router.get('/lastMonthUsedfunds', async(ctx) => {
    var date = new Date();
    var date_ = dateFormat(date, 'yyyy/mm/') + 01;
    date = new Date(date_);
    date.setDate(date.getDate() -1);
    var edate = dateFormat(date, 'yyyymmdd');
    var bdate = edate.substr(0, 6) + '01';
    console.log(  bdate + ','+ edate);  
    
    ctx.response.type = 'json';
    let data = await ctx.db.collection('t86').aggregate([
        {
            $match:{
                $and:[
                    {date:{'$gte':bdate, '$lte':edate}},
                    {groupCode:{'$ne':'00'}}
                ]
            }
        },
        {
            $group:{
                _id: {
                    date:{$substr:['$date', 0, 4]}
                  , groupCode:'$groupCode'
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
    ]).toArray();
        
    ctx.response.body = data;
});


//==================test==================
router.get('/KlineH', async(ctx) => {
    let code = ctx.request.query.code;
    await ctx.render('KlineH', {
        msg:'stock:' + code
    })
});

module.exports = router;