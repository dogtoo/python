const router = require('koa-router')();

// Router -> /
router.get('/kline', async(ctx) => {
    console.log(`   getT86`);
    let code = ctx.request.query.code;
    await ctx.render('kline', {
        msg:'stock:' + code
    })
});

router.get('/absPainter.js', async(ctx) => {
    await ctx.render('js/absPainter')
});

router.get('/axis-x.js', async(ctx) => {
    await ctx.render('js/axis-x')
});

router.get('/axis-y.js', async(ctx) => {
    await ctx.render('js/axis-y')
});

module.exports = router;