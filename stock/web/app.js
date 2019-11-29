const Koa = require('koa');
const logger = require('koa-logger');
const Router = require('koa-router');
const bodyParser = require('koa-bodyparser');
const views = require('koa-views');
const compose = require('koa-compose');
/* 3. read html file test
const fs = require('fs');
const path = require('path');
*/
const router = Router();
const app = new Koa();
app.use(logger())
app.use(bodyParser());
app.use(views(__dirname, {
        extension: 'html'
    })
);

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

router.get('/login', async(ctx) => {
    console.log(`get login`);
    ctx.body = `
        <form method="POST" action="/login">
            <label>UserName</label>
            <input name="user" /><br/>
            <button type="submit">submit</button>
        </form>
    `;
});

router.post('/login', async(ctx) => {
    console.log(`post login`);
    let user = ctx.request.body.user;
    ctx.body = `<p>Welocome,${user}!</p>`;
});

// Router -> /
router.get('/', async(ctx) => {
    console.log(`get /`);
    await ctx.render('index')
});

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

//不知為什這個要放在router設定的後面
app.use(router.routes());

app.listen(3000);