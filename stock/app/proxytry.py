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
handlers = [logging.FileHandler('../../log/proxytry.log', 'w', 'utf-8')]
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
    run = 0
    while True:
        proxy = await proxies.get()
        if proxy is None: break
        #print('Found proxy: %s' % proxy)  
        #logging.info(str(proxy.types) + ' ' + str(proxy.host) + ':' + str(proxy.port))
        #httpType = ''
        #if 'HTTP' in proxy.types:
        #    httpType = 'http' 
        #else:
        #    httpType = 'https' 
        httpType = 'http' 
        p={};
        p[httpType] = str(proxy.host) + ':' + str(proxy.port)
        #logging.info(p)
        try:
            req = requests.Session()
            adapter = SSLContextAdapter()
            req.mount(SESSION_URL, adapter)
            req.get(SESSION_URL, proxies=p, timeout=(5, 5), verify=True)
            logging.info("proxy ok :" + str(p['http']))
            stockCodeL = ['1101']
            stock = twstock.realtime.get(stockCodeL, req, p, logging)
        except BaseException as e:
            logging.error("proxy fal :" + str(p['http']))
            logging.error("proxy fal :" + str(e))
        run = run + 1
        if run == 10:
            time.sleep(5)
            run = 0

proxies = asyncio.Queue()
broker = Broker(proxies)
tasks = asyncio.gather(
    broker.grab(countries=['US', 'GB', 'DE', 'FR', 'ID', 'ZA', 'TH', 'CN', 'AR', 'CA', 'IT', 'JP', 'TW', 'HK', 'KR']),
    show(proxies))

loop = asyncio.get_event_loop()
loop.run_until_complete(tasks)

