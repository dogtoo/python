const router = require('koa-router')();

// Router -> /
router.get('/kline', async(ctx) => {
    console.log(`   getT86`);
    let code = ctx.request.query.code;
    await ctx.render('kline', {
        msg:'stock:' + code
    })
});

router.get('/js/absPainter.js', async(ctx) => {
    await ctx.render('js/absPainter')
});

router.get('/js/axis-x.js', async(ctx) => {
    await ctx.render('js/axis-x')
});

router.get('/js/axis-y.js', async(ctx) => {
    await ctx.render('js/axis-y')
});

router.get('/js/k-data.js', async(ctx) => {
    await ctx.render('js/k-data')
});

module.exports = router;