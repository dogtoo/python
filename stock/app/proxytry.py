#!/usr/bin/python
#coding:utf-8
import twstock
import pymongo
import time
import sys
import logging
import requests
from datetime import timedelta, date, datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

import asyncio
from proxybroker import Broker

SESSION_URL = 'https://mis.twse.com.tw/stock/api/getStockInfo.jsp'
handlers = [logging.FileHandler('/python/log/proxytry.log', 'w', 'utf-8')]
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s : %(message)s',
                    datefmt='%Y-%m-%dT %H:%M:%S',
                    handlers=handlers)
                    #filename='../../log/proxytry.log' )
                    #filename='/python/log/proxytry.log' )

class SSLContextAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        kwargs['ssl_context'] = context
        context.load_default_certs() # this loads the OS defaults on Windows
        return super(SSLContextAdapter, self).init_poolmanager(*args, **kwargs)

async def show(proxies):
    while True:
        logging.info('6')
        proxy = await proxies.get()
        logging.info('7')
        if proxy is None: break
        logging.info('8')
        print('Found proxy: %s' % proxy)  
        #logging.info(str(proxy.types) + ' ' + str(proxy.host) + ':' + str(proxy.port))
        #httpType = ''
        #if 'HTTP' in proxy.types:
        #    httpType = 'http' 
        #else:
        #    httpType = 'https' 
        #p={};
        #p[httpType] = str(proxy.host) + ':' + str(proxy.port)
        #logging.info(p)
        #try:
        #    req = requests.Session()
        #    adapter = SSLContextAdapter()
        #    req.mount(SESSION_URL, adapter)
        #    req.get(SESSION_URL, proxies=p, timeout=(5, 5), verify=True)
        #    logging.debug("proxy ok :" + str(p['http']))
        #    stockCodeL = ['1101']
        #    stock = twstock.realtime.get(stockCodeL, req, p, logging)
        #    logging.debug("proxy stock:" + str(stock))        
        #except BaseException as e:
        #    logging.error("proxy fal :" + str(e))

try:
    logging.info('1')
    proxies = asyncio.Queue()
    logging.info('2')
    broker = Broker(proxies)
    logging.info('3')
    tasks = asyncio.gather(
        broker.find(types=['HTTP', 'HTTPS'], limit=10),
        show(proxies))

    logging.info('4')
    loop = asyncio.get_event_loop()
    logging.info('5')
    loop.run_until_complete(tasks)
    logging.info('6')
except BaseException as e:
    logging.error("Broker :" + str(e))
