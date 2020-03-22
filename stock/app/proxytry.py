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
import json

SESSION_URL = 'https://mis.twse.com.tw/'
#SESSION_URL = 'http://icanhazip.com/'
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

#async def show(proxies):
#    run = 0
#    while True:
#        proxy = await proxies.get()
#        if proxy is None: break
#        #print('Found proxy: %s' % proxy)  
#        #logging.info(str(proxy.types) + ' ' + str(proxy.host) + ':' + str(proxy.port))
#        #httpType = ''
#        #if 'HTTP' in proxy.types:
#        #    httpType = 'http' 
#        #else:
#        #    httpType = 'https' 
#        httpType = 'http' 
#        p={};
#        p[httpType] = str(proxy.host) + ':' + str(proxy.port)
#        logging.info(p)
#        try:
#            req = requests.Session()
#            adapter = SSLContextAdapter()
#            req.mount(SESSION_URL, adapter)
#            req.get(SESSION_URL, proxies=p, timeout=(5, 5), verify=True)
#            logging.info("proxy ok :" + str(p['http']))
#            stockCodeL = ['1316','1708','1709','1710','1711','1712','1713','1714','1717','1718','1721','1722','1723','1724','1725','1726','1727','1730','1732','1735','1773','1776','3708','4720','4722','4725','4739','4755','4763','4764','4766','1598','1701','1707','1720','1731','1733','1734','1736','1760','1762','1783','1786','1789','3164','3705','4104','4106','4108','4119','4133','4137','4141','4142','4144','4148','4155','4164','4190','4737','4746','6452','6541','6666','2616','6505','8926','9908','9918','9926','9931','9937','2302','2303','2329','2330','2337','2338','2342','2344','2351','2363','2369','2379','2388','2401','2408','2434','2436','2441','2449','2451','2454','2458','2481','3006','3014','3016','3034','3035','3041','3054','3094','3189','3257','3413','3443','3519','3530','3532','3536','3545','3579','3583','3588','3661','3686','3711','4919','4952','4961','4967','4968','5269','5285','5305','5471','6202','6239','6243','6257','6271','6415','6451','6525','6531','6533','6552','6573','8016','8028','8081','8110','8131','8150','8261','8271','1504','1506','1507','1512','1513','1514','1515','1517','1519','1521','1522','1524','1525','1526','1527','1528','1529','1530','1533']
#            stock = twstock.realtime.get(stockCodeL, req, p, logging)
#            logging.info(len(stock))
#        except BaseException as e:
#            logging.error("proxy fal :" + str(p['http']))
#            logging.error("proxy fal :" + str(e))
#        run = run + 1
#        if run == 6:
#            run = 0
#            logging.info('sleep')
#            time.sleep(3)
#
#proxies = asyncio.Queue()
#broker = Broker(proxies)
#tasks = asyncio.gather(
#    broker.grab(countries=['US', 'GB', 'JP', 'TW', 'HK', 'KR', 'DE', 'FR', 'CN', 'CA', 'ID', 'ZA', 'TH', 'AR', 'IT']),
#    show(proxies))
#
#loop = asyncio.get_event_loop()
#loop.run_until_complete(tasks)

run = 0
while True:
    try:
        req = requests.Session()
        adapter = SSLContextAdapter()
        req.mount(SESSION_URL, adapter)
        #res = req.get(SESSION_URL, timeout=(5, 5), verify=True)
        #logging.info("session ok ")
        proxy = {}
        stockCodeL = ['1316','1708','1709','1710','1711','1712','1713','1714','1717','1718','1721','1722','1723','1724','1725','1726','1727','1730','1732','1735','1773','1776','3708','4720','4722','4725','4739','4755','4763','4764','4766','1598','1701','1707','1720','1731','1733','1734','1736','1760','1762','1783','1786','1789','3164','3705','4104','4106','4108','4119','4133','4137','4141','4142','4144','4148','4155','4164','4190','4737','4746','6452','6541','6666','2616','6505','8926','9908','9918','9926','9931','9937','2302','2303','2329','2330','2337','2338','2342','2344','2351','2363','2369','2379','2388','2401','2408','2434','2436','2441','2449','2451','2454','2458','2481','3006','3014','3016','3034','3035','3041','3054','3094','3189','3257','3413','3443','3519','3530','3532','3536','3545','3579','3583','3588','3661','3686','3711','4919','4952','4961','4967','4968','5269','5285','5305','5471','6202','6239','6243','6257','6271','6415','6451','6525','6531','6533','6552','6573','8016','8028','8081','8110','8131','8150','8261','8271','1504','1506','1507','1512','1513','1514','1515','1517','1519','1521','1522','1524','1525','1526','1527','1528','1529','1530','1533']
        stock = twstock.realtime.get(stockCodeL, req, proxy, logging)
        logging.info(len(stock))
    except BaseException as e:
        logging.error("proxy fal :" + str(e))
    run = run + 1
    if run == 7:
        run = 0
        logging.info('sleep')
        time.sleep(3)
