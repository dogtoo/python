const router = require('koa-router')();

// Router -> /
router.get('/getT86', async(ctx) => {
    console.log(`   getT86`);
    let code = ctx.request.query.code;
    await ctx.render('index', {
        msg:'stock:' + code
    })
});

module.exports = router;