const Koa = require('koa');
//const yaml_config = require('node-yaml-config');
//const config = yaml_config.load('../config.ini');
const logger = require('koa-logger');
//const Router = require('koa-router');
const bodyParser = require('koa-bodyparser');
const views = require('koa-views');
const compose = require('koa-compose');
const mongo = require('koa-mongo');
/* 3. read html file test
const fs = require('fs');
const path = require('path');
*/
//console.log(config.server);
const router = require('./routes/index');
const app = new Koa();

app.use(logger())
app.use(bodyParser());
app.use(views(__dirname + '/views', {
        extension: 'ejs'
    })
);

/*
app.use(views(__dirname + '/views/js', {
        extension: 'js'
    })
);*/
app.use(mongo({
    //host: '219.85.16.213',
    host: '192.168.1.5',
    port: 27017,
    db: 'twStock',
    user: 'twstock',
    pass: 'twstock123',
    authSource: 'twStock'
}));

/**
Middleware組合 Star
**/
/* 未使用koa-compose
app.use(async function(ctx,next) {
    const start_time = Date.now();
    console.log(`start ${ctx.method} ${ctx.url}`);
    await next();
    const ms = Date.now() - start_time;
    console.log(`end ${ctx.method} ${ctx.url} - ${ms}ms`);
});
*/

async function log_(ctx, next) {
    const start_time = Date.now();
    console.log(`log_ start`);
    await next();
    const ms = Date.now() - start_time;
    console.log(`log_ end ${ctx.method} ${ctx.url} - ${ms}ms`);
}

async function test_(ctx, next) {
    const start_time = Date.now();
    console.log(`test_ start`);
    console.log(ctx.request.query);
    await next();
    const ms = Date.now() - start_time;
    console.log(`test_ end ${ctx.method} ${ctx.url} - ${ms}ms`);
}

/**
Middleware End
**/

//將Middleware放到koa app
const middlewares = compose([log_, test_]);
app.use(middlewares)

app.use(router.routes(), router.allowedMethods());

app.listen(3000);
/* 3. read html file test
router.get('/', async(ctx) => {
    ctx.body = render('index.html');
});
function render(filename) {
    let fullpath = path.join(__dirname, filename)
    return fs.readFileSync(fullpath, 'binary')
}
*/

/* 2. Router test
// Router -> /
router.get('/', async(ctx) => {
    const start_time = Date.now();
    ctx.body = 'Hello Koa2 body';
    const ms = Date.now() - start_time;
    console.log(`${ctx.method} ${ctx.url} - ${ms}ms`);
});
// Router -> /ready
router.get('/ready', async(ctx) => {
    const start_time = Date.now();
    let name = ctx.query.name;
    let talk = ctx.query.talk;
    ctx.body = `<p>${name}：${talk}</p>`;
    const ms = Date.now() - start_time;
    console.log(`${ctx.method} ${ctx.url} - ${ms}ms`);
});
*/
