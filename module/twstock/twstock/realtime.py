# -*- coding: utf-8 -*-

import datetime
import json
import time
import requests
import twstock
import sys
import logging

#SESSION_URL = 'http://mis.twse.com.tw/stock/index.jsp'
#STOCKINFO_URL = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={stock_id}&_={time}'
SESSION_URL = 'https://mis.twse.com.tw/stock/index.jsp'
STOCKINFO_URL = 'https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={stock_id}&_={time}'

# Mock data
mock = False
req = requests
prox = {}
#https://sites.google.com/site/kentyeh2000/zheng-jiao-suo-ji-shi-zi-xun-jie-xi
def _format_stock_info(data) -> dict:
    result = {
        'timestamp': 0.0,
        'info': {},
        'realtime': {}
    }
        
    result['code'] = data['c'] #股票代碼
    result['date'] = data['d'] #交易日期
    result['time'] = data['t'] #揭示時間
    try:
        if 'ot' in data:
            result['final_time'] = data['ot'] #最後交易時間
        else:
            result['final_time'] = data['t']
        if 'fv' in data:
            result['final_trade_volume'] = int(data['fv']) #盤後交易量
        result['stock_type'] = data['ex'] #上市(tes) / 上櫃(otc)

        # Information
        result['info']['code'] = data['c']
        result['info']['channel'] = data['ch']
        result['info']['name'] = data['n']
        result['info']['fullname'] = data['nf']
        
        if 'tlong' not in data:
            result['success'] = False
            return result

        # Timestamp
        result['timestamp'] = int(data['tlong']) / 1000 #unix timestamp
        result['info']['time'] = datetime.datetime.fromtimestamp(
            int(data['tlong']) / 1000).strftime('%Y-%m-%d %H:%M:%S')

        # Process best result
        def _split_best(d):
            if d:
                return list(map(float, d.strip('_').split('_')))
            return d

        # Realtime information
        if 'z' in data:
            result['realtime']['latest_trade_price'] = float(data.get('z', None)) #最後成交價
        if 'tv' in data:
            result['realtime']['trade_volume'] = int(data.get('tv', None)) #當盤成交量
        if 'v' in data:    
            result['realtime']['accumulate_trade_volume'] = int(data.get('v', None)) #累積成交量
        #最佳五檔
        if 'b' in data:
            result['realtime']['best_bid_price'] = _split_best(data.get('b', None)) #買進價格
        if 'g' in data:    
            result['realtime']['best_bid_volume'] = _split_best(data.get('g', None)) #買進數量
        if 'a' in data:
            result['realtime']['best_ask_price'] = _split_best(data.get('a', None)) #賣出價格
        if 'f' in data:
            result['realtime']['best_ask_volume'] = _split_best(data.get('f', None)) #賣出數量
        
        if 'o' in data:
            result['realtime']['open'] = float(data.get('o', None)) #開盤
        if 'h' in data:
            result['realtime']['high'] = float(data.get('h', None)) #最高
        if 'l' in data:
            result['realtime']['low'] = float(data.get('l', None)) #最低

        # Success fetching
        result['success'] = True
    except:
        result['success'] = False
        
    return result
    
def _join_stock_id(stocks) -> str:
    if isinstance(stocks, list):
        return '|'.join(['{}_{}.tw'.format(
            'tse' if s in twstock.twse else 'otc', s) for s in stocks])
    return '{}_{stock_id}.tw'.format(
        'tse' if stocks in twstock.twse else 'otc', stock_id=stocks)


def get_raw(stocks, req) -> dict:
    try:
        #req = requests.Session()
        #req.get(SESSION_URL)
        logging.debug(STOCKINFO_URL.format(
                stock_id=_join_stock_id(stocks),
                time=int(time.time()) * 1000))
        r = req.get(
            STOCKINFO_URL.format(
                stock_id=_join_stock_id(stocks),
                time=int(time.time()) * 1000), proxies=prox)
        if sys.version_info < (3, 5):
            try:
                #logging.debug(r.json())
                return r.json()
            except ValueError:
                return {'rtmessage': 'json decode error', 'rtcode': '5000'}
        else:
            try:
                #logging.debug(r.json())
                return r.json()
            except json.decoder.JSONDecodeError:
                return {'rtmessage': 'json decode error', 'rtcode': '5000'}
    except requests.ConnectionError as e:
        return {'rtmessage': 'ConnectionError:'  + str(e), 'rtcode': '5000'}
    except requests.exceptions.RequestException as e:
        return {'rtmessage': 'RequestException: ' + str(e), 'rtcode': '5000'}
    except BaseException as e:
        return {'rtmessage': 'BaseException: ' + str(e), 'rtcode': '5000'}

def get(stocks, request, proxies, logging, retry=0):
    # Prepare data
    prox = proxies
    #req = request
    data = get_raw(stocks, request) if not mock else twstock.mock.get(stocks)

    # Set success
    data['success'] = False

    # JSONdecode error, could be too fast, retry
    if data['rtcode'] == '5000':
        # XXX: Stupit retry, you will dead here
        if retry:
            logging.info('retry:' + str(retry) + ' because:' + str(data['rtmessage']))
            return get(stocks, request, proxies, logging, retry - 1)
        return data

    # No msgArray, dead
    if 'msgArray' not in data:
        return data

    # Check have data
    if not len(data['msgArray']):
        data['rtmessage'] = 'Empty Query.'
        data['rtcode'] = '5001'
        return data
    # Return multiple stock data
    if isinstance(stocks, list):
        result = {
            data['info']['code']: data for data in map(_format_stock_info, data['msgArray'])
        }
        result['success'] = True
        return result
    return _format_stock_info(data['msgArray'][0])
