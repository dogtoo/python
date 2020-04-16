const router = require('koa-router')();
const dateFormat = require('dateformat');
// Router -> /

router.get('/crossline', async(ctx) => {
    let code = ctx.request.query.code;
    await ctx.render('crossline')
});

router.get('/crossline_axis_seq', async(ctx) => {
    let code = ctx.request.query.code;
    await ctx.render('crossline_axis_seq')
});

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
    //let trendCodeList = ctx.request.body.trendCodeList;
    let code = ctx.request.body.code;
    let stock_market = ctx.request.body.stockMarket;
    
    let date;
    if (typeof ctx.request.body.date === 'undefined') {
        date = new Date();
        date = dateFormat(date, 'yyyymmdd');
    }
    else {
        date = ctx.request.body.date;
    }
    
    //let codeList = [];
    //if (typeof trendCodeList != 'undefined') {
    //    for (let i in trendCodeList) {
    //        let code_ = trendCodeList[i]['code'];
    //        let market_ = trendCodeList[i]['market'];
    //        codeList.append({'code':code_, 'mark':market_});
    //    }
    //}
    //else 
    //{
    //    codeList.append({'code':code, 'market':stock_market});
    //}
    
    //for (let i in codeList) {
        console.log('code:'+code+',date:'+date+',market:'+stock_market);
        //if (code === undefined) code = '1101';
        //if (date === undefined) date = '20200211';
        
        ctx.response.type = 'json';
        let trand = await ctx.db.collection('realtime').aggregate([
            {
                $match:{
                    $and:[
                        {code:{'$eq':code}
                       , date:{'$eq':date}
                       , time:{'$gte':'09:00:00'}
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
                    'best_bid_price':{$arrayElemAt:['$best_bid_price', 0]},
                    'acc_vol':'$accumulate_trade_volume',
                    'vol':'$trade_volume'
               }
            }, {
                $sort:{
                    'time':1
                }
            }
        ]).toArray();
        
        if (parseInt(trand[0].time.substr(1, 2)) < 9) {
            trand.shift();
        }
        
        
        let ftrand = await ctx.db.collection('stockDay').aggregate([
            {
                $match:{
                    $and:[
                        {code:{'$eq':code}
                       , date:{'$lt':date}
                        }
                    ]            
                }
            }, {
                $sort: {
                    'date':-1
                }
            }, {
                $project:{
                    '_id':0,
                    'time':'09:00:00',
                    'price':'$Closing_Price',
                    'vol':'0'
               }
            }, {$limit:1}
        ]).toArray();
        
        trand.unshift(ftrand[0]);
        
        let info = await ctx.db.collection(stock_market).find({'code':code},{'_id':0,'type':1}).toArray();
        data = {'trand':trand, 'info':info[0]}
    //}
    ctx.response.body = data;
});

router.get('/Trend', async(ctx) => {
    let code = ctx.request.query.code;
    await ctx.render('Trend', {
        msg:'stock:' + code
    })
});

router.get('/funds', async(ctx) => {
    var date = new Date();
    let edate = dateFormat(date, 'yyyy/mm/dd');
    
    var date_ = dateFormat(date, 'yyyy/mm/') + 01;
    date = new Date(date_);
    date.setDate(date.getDate() -1);
    //date.setYear(date.getFullYear() -1);
    //var m = date.getMonth() + 2;
    var m = date.getMonth()-3;
    date.setMonth(m, 1);
    let bdate = dateFormat(date, 'yyyy/mm/dd');
    console.log(  bdate + ','+ edate);  
    await ctx.render('funds', {
        bdate: bdate,
        edate: edate
    })
});
//取得上月外資可用資金
router.post('/lastMonthUsedfunds', async(ctx) => {
    let bdate = ctx.request.body.bdate;
    let edate = ctx.request.body.edate;
    let groupType = ctx.request.body.groupType;
    let fundsType = ctx.request.body.fundsType;
    
    let group_ = ctx.request.body.group;
    let stockCode_ = ctx.request.body.stockCode;
    let fundsGroup_ = ctx.request.body.fundsGroup;
    
    if (typeof bdate === 'undefined' || typeof edate === 'undefined') {
        let date = new Date();
        let date_ = dateFormat(date, 'yyyy/mm/') + 01;
        date = new Date(date_);
        date.setDate(date.getDate() -1);
        edate = dateFormat(date, 'yyyymmdd');
        /*
        date.setYear(date.getFullYear() -1);
        var m = date.getMonth() + 1;*/
        let m = date.getMonth()
        date.setMonth(m, 1);
        bdate = dateFormat(date, 'yyyymmdd');
    }
    console.log(  bdate + ','+ edate + ',' + group_ + ',' + stockCode_ + ',' + fundsGroup_);  
    
    ctx.response.type = 'json';    
    
    let match = {$match:{}};
    let matchAnd = [
            {date:{'$gte':bdate, '$lte':edate}},
            {groupCode:{'$ne':'00'}}
        ];
    if (typeof group_ != 'undefined' && group_.match(/group|allGroup/) && stockCode_ != '') matchAnd.push({groupCode:{'$in':stockCode_.match(/\d{2}/g)}});
    if (typeof group_ != 'undefined' && group_ === 'stock' && stockCode_ != '') matchAnd.push({code:{'$in':stockCode_.match(/\d{4}/g)}});
    match.$match = {'$and':matchAnd};

    let groupDateCnt = 4; //年
    if (typeof fundsGroup_ != 'undefined' && fundsGroup_ === 'monthGroup') groupDateCnt = 6;
    if (typeof fundsGroup_ != 'undefined' && fundsGroup_ === 'dayGroup') groupDateCnt = 8;
    let group = {
            $group:{
                _id:{date:{$substr:['$date', 0, groupDateCnt]}}
               ,'FII_I':{$sum:'$FII_I'}
               ,'FII_O':{$sum:'$FII_O'}
               ,'SIT_I':{$sum:'$SIT_I'}
               ,'SIT_O':{$sum:'$SIT_O'}
               ,'DProp_I':{$sum:'$DProp_I'}
               ,'DProp_O':{$sum:'$DProp_O'}
               ,'DHedge_I':{$sum:'$DHedge_I'}
               ,'DHedge_O':{$sum:'$DHedge_O'}
            }
        };
    
    if (typeof group_ != 'undefined' && group_.match(/allGroup/) ) group.$group._id['groupCode'] = '$groupCode';
    if (typeof group_ != 'undefined' && group_.match(/group|stock/)) {
        group.$group._id['groupCode'] = '$groupCode';
        group.$group._id['code'] = '$code';
    }
    //if (typeof group_ != 'undefined' && group_ = 'stock') group.$group._id['groupCode'] = '$groupCode';
    
    let lookup = {$lookup:{
        from: 'TWSE',
        let: {groupCode:'$_id.groupCode'},
        pipeline:[
            { 
                $match: {
                    $expr: {
                        $eq: [ '$groupCode', '$$groupCode']
                    }
                }
            },
            { $project: { group:1, _id:0}},
            { $limit:1}
        ],
        as:'groupName'
    }};
    
    if (typeof group_ != 'undefined' && group_.match(/group|stock/)) {
        lookup.$lookup.let = {code:'$_id.code'};
        lookup.$lookup.pipeline[0].$match.$expr.$eq = ['$code', '$$code'];
        lookup.$lookup.pipeline[1].$project['name'] = 1;
    }
    
    let lookupTP = {$lookup:{
        from: 'TPEX',
        let: {groupCode:'$_id.groupCode'},
        pipeline:[
            { 
                $match: {
                    $expr: {
                        $eq: [ '$groupCode', '$$groupCode']
                    }
                }
            },
            { $project: { group:1, _id:0}},
            { $limit:1}
        ],
        as:'groupNameTP'
    }};
    
    if (typeof group_ != 'undefined' && group_.match(/group|stock/)) {
        lookupTP.$lookup.let = {code:'$_id.code'};
        lookupTP.$lookup.pipeline[0].$match.$expr.$eq = ['$code', '$$code'];
        lookupTP.$lookup.pipeline[1].$project['name'] = 1;
    }
    
    let project = {$project: {
                _id: 0
               ,date: '$_id.date'
               ,groupCode: '$_id.groupCode'
               ,groupName: [{$arrayElemAt:["$groupName.group",0]},{$arrayElemAt: ["$groupNameTP.group",0]}]
               ,'FII_I':'$FII_I'
               ,'FII_O':'$FII_O'
               ,'FII_diff':{$subtract:['$FII_I', '$FII_O']}
               ,'SIT_I':'$SIT_I'
               ,'SIT_O':'$SIT_O'
               ,'SIT_diff':{$subtract:['$SIT_I', '$SIT_O']}
               ,'DProp_I':'$DProp_I'
               ,'DProp_O':'$DProp_O'
               ,'DHedge_I':'$DHedge_I'
               ,'DHedge_O':'$DHedge_O'
               /*,'外資買進':'$FII_I'
               ,'外資賣出':'$FII_O'
               ,'外資增減':{$subtract:['$FII_I', '$FII_O']}
               ,'投信買進':'$SIT_I'
               ,'投信賣出':'$SIT_O'
               ,'投信增減':{$subtract:['$SIT_I', '$SIT_O']}
               ,'自營商買進':'$DProp_I'
               ,'自營商賣出':'$DProp_O'
               ,'自營商買進避':'$DHedge_I'
               ,'自營商賣出避':'$DHedge_O'*/
            }
        };
    if (typeof group_ != 'undefined' && group_.match(/group|stock/)) {
        project.$project.groupCode = '$_id.code';
        project.$project.groupName = '$groupName.name';
    }
        
    let sort = {
            $sort:{
                'date':1
            }
        };
    
    let args = [match, group, {
            $sort:{
                '_id':1
            }
        }, lookup, lookupTP, project, sort];
    console.log(JSON.stringify(args, null, 4));
    let data = await ctx.db.collection('t86').aggregate(args).toArray();
    let out = {};
    let date_ = ' ';
    //var FII_I_T = 0, FII_O_T = 0;
    
    //var I_ = 0, O_ = 0, S_ = 0, fv_ = 0;
    //var I_T = 0, O_T = 0, S_T = 0, fv_T = 0;
    let fv_ = 0, fv_T = 0;
    let codeL_ = [];
    let groupH_ = {};
        
    for (let i in data) {
        //console.log(data[i].groupName[1]);
        groupH_[data[i].groupCode] = (data[i].groupName[0] != null) ? data[i].groupName[0] : data[i].groupName[1];
        let row = data[i];
        if (row.date != date_) {
            if (date_ != ' ') {
                //out[date_]['FII_I_T'] = FII_I_T;
                //out[date_]['FII_O_T'] = FII_O_T;
                out[date_]['FII_I_T'] = fv_T;
            }
            //FII_I_T = 0, FII_O_T = 0;
            //I_T = 0, O_T = 0, S_T = 0;
            fv_T = 0;
            date_ = row.date;
        }
        //FII_I_T += row.FII_I;
        //FII_O_T += row.FII_O;
        if (fundsType === 'buy') {
            if (groupType.match(/F/))
                fv_ += row.FII_I;
            if (groupType.match(/O/))
                fv_ += row.SIT_I;
            if (groupType.match(/S/))
                fv_ += row.DProp_I + row.DHedge_I;
        } else if (fundsType === 'sel') {
            if (groupType.match(/F/))
                fv_ += row.FII_O;
            if (groupType.match(/O/))
                fv_ += row.SIT_O;
            if (groupType.match(/S/))
                fv_ += row.DProp_O + row.DHedge_O;
        } else if (fundsType === 'sum') {
            if (groupType.match(/F/))
                fv_ += row.FII_diff;
            if (groupType.match(/O/))
                fv_ += row.SIT_diff;
        }
        
        //I_T += I_;
        //O_T += O_;
        //S_T += S_;
        fv_T += fv_;
        if (typeof out[row.date] === 'undefined')
            out[row.date] = {};
        if (typeof out[row.date]['group'] === 'undefined')
            out[row.date] = { 'group':[] };
        out[row.date].group.push({
            'group': row.groupCode + ((row.groupName[0] != null) ? row.groupName[0] : row.groupName[1]),
            //'FII_I': row.FII_I,
            //'FII_O': row.FII_O
            'FII_I': fv_
        });
        //I_ = 0, O_ = 0, S_ = 0;
        fv_ = 0;
    }
    
    //out[date_].FII_I_T = FII_I_T;
    //out[date_].FII_O_T = FII_O_T;
    out[date_].FII_I_T = fv_T;
    
    Object.keys(groupH_).sort().forEach(function(key) {
        codeL_.push(key + groupH_[key]);
    });
    Object.keys(out).sort().forEach(function(key) {
        let l_ = out[key].group;
        //console.log(l_);
        for (let i in codeL_) {
            if (i >= l_.length)
                l_.splice(i, 0, {group:codeL_[i], FII_I: 0});
            else if ((codeL_[i].match(/^\d+/))[0] != (l_[i].group.match(/^\d+/))[0]) {
                l_.splice(i, 0, {group:codeL_[i], FII_I: 0});
            }
        }
    });
    out['lrowG'] = codeL_;
    /*
    var I_P = 0, O_P = 0;
    for (var d in out) {
        for (var i in out[d].group) {
            var r = out[d].group[i];
            r.FII_I_P = Math.floor((r.FII_I / out[d].FII_I_T) * 10000) / 100;
            r.FII_O_P = Math.floor((r.FII_O / out[d].FII_O_T) * 10000) / 100;
            I_P += r.FII_I_P;
            O_P += r.FII_O_P;
        }
    }
    console.log(I_P + ',' + O_P);*/
    ctx.response.body = out;
});


//==================test==================
router.get('/KlineH', async(ctx) => {
    let code = ctx.request.query.code;
    await ctx.render('KlineH', {
        msg:'stock:' + code
    })
});

module.exports = router;