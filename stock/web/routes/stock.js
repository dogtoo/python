const router = require('koa-router')();

// Router -> /
router.get('/kline', async(ctx) => {
    let code = ctx.request.query.code;
    await ctx.render('kline', {
        msg:'stock:' + code
    })
});

router.get('/crossline', async(ctx) => {
    let code = ctx.request.query.code;
    await ctx.render('crossline')
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