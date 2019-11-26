import datetime
import json
import time
import requests
import twstock
import sys
import logging
#http://www.twse.com.tw/fund/T86?response=json&date=20190528&selectType=01&_=1559145215220
#https://www.twse.com.tw/fund/TWT47U?response=json&date=20030101&selectType=01&_=1574739645853 月報 101/5/2前改用月報 date 放每月1日
#https://godoc.org/github.com/toomore/gogrs/twse go的方式取股票

global date_v
date_v = datetime.datetime.now().strftime("%Y%m%d")
log = logging
def _format_stock_info(data) -> dict:
    result = {
        'code': ''
      , 'date': ''
      , 'FII_I': 0 #外資買進
      , 'FII_O': 0 #外資賣出
      , 'SIT_I': 0 #投信買進
      , 'SIT_O': 0 #投信賣出
      , 'DProp_I': 0 #自營商(自行買賣)
      , 'DProp_O': 0 #自營商(自行買賣)
      , 'DHedge_I': 0 #自營商(避險)
      , 'DHedge_O': 0 #自營商(避險)
    }
    
    result['code'] = data[0]
    result['date'] = ''
    if len(data) == 12:
        result['FII_I'] = int(data[2].replace(',',''))
        result['FII_O'] = int(data[3].replace(',',''))
        result['SIT_I'] = int(data[5].replace(',',''))
        result['SIT_O'] = int(data[6].replace(',',''))
        result['DProp_I'] = int(data[9].replace(',',''))
        result['DProp_O'] = int(data[10].replace(',',''))
        result['DHedge_I'] = 0
        result['DHedge_O'] = 0
    elif len(data) == 16:
        result['FII_I'] = int(data[2].replace(',',''))
        result['FII_O'] = int(data[3].replace(',',''))
        result['SIT_I'] = int(data[5].replace(',',''))
        result['SIT_O'] = int(data[6].replace(',',''))
        result['DProp_I'] = int(data[9].replace(',',''))
        result['DProp_O'] = int(data[10].replace(',',''))
        result['DHedge_I'] = int(data[12].replace(',',''))
        result['DHedge_O'] = int(data[13].replace(',',''))
    elif len(data) == 19:
        result['FII_I'] = int(data[2].replace(',','')) + int(data[5].replace(',',''))
        result['FII_O'] = int(data[3].replace(',','')) + int(data[6].replace(',',''))
        result['SIT_I'] = int(data[8].replace(',',''))
        result['SIT_O'] = int(data[9].replace(',',''))
        result['DProp_I'] = int(data[12].replace(',',''))
        result['DProp_O'] = int(data[13].replace(',',''))
        result['DHedge_I'] = int(data[15].replace(',',''))
        result['DHedge_O'] = int(data[16].replace(',',''))
    
    return result

def dataChk(res):
    if 'stat' in res and res['stat'] == 'OK':
        datalist = res['data']
        for d in datalist:
            #log.debug('       len = ' + str(len(d)))
            if int(res['date']) <= 20141128 and len(d) != 12:
                log.error('       len = ' + str(len(d)))
                return False
            elif int(res['date']) > 20141128 and int(res['date']) <= 20171215 and len(d) != 16:
                log.error('       len = ' + str(len(d)))
                return False            
            elif int(res['date']) > 20171215 and len(d) != 19:
                log.error('       len = ' + str(len(d)))
                return False
    return True

def get_raw(group, date, resType, proxies) -> dict:
    try:
        if int(date) < 20120501:
            STOCKINFO_URL = 'https://www.twse.com.tw/fund/TWT47U'
        else:
            STOCKINFO_URL = 'http://www.twse.com.tw/fund/T86'
    
        """
        proxies = {
            "http": "http://105.235.203.114:8080",
            "https": "http://105.235.203.114:8080",
        }
        """
        i = 0
        res = {'rtmessage': 'get error', 'rtcode': 1}
        while i < 10:
            req = requests
            #req.keep_alive = False
            """
            if 'http' in proxies:
                log.debug('       proxy get session begin')
                req.get(STOCKINFO_URL, proxies=proxies, timeout=(5, 20))
                log.debug('       proxy get session end')
            else:
                log.debug('       get session begin')
                req.get(STOCKINFO_URL, timeout=(5, 20))
                log.debug('       get session end')
            time.sleep(1)
            """
            t=int(time.time()) * 1000
            p = {'response': resType, 'date': date, 'selectType':group, '_':t}
                
            if 'http' in proxies:
                log.debug('       proxy get data begin')
                res = req.get(STOCKINFO_URL, proxies=proxies, params=p, timeout=(5, 80))
                log.debug('       proxy get data end')
            else:
                log.debug('       get data begin')
                res = req.get(STOCKINFO_URL, params=p, timeout=(5, 80))
                log.debug('       get data end')
            
            if 'status_code' in res and res.status_code != 200:
                res = {'rtmessage': str(res.status_code), 'rtcode': 1}
                break
            
            if sys.version_info < (3, 5):
                try:
                    res = res.json()
                    log.debug('       res.json')
                except ValueError:
                    res = {'rtmessage': 'json decode error:' + str(res), 'rtcode': 1}
                    break
            else:
                try:
                    res = res.json()
                    log.debug('       res.json')
                except json.decoder.JSONDecodeError:
                    res = {'rtmessage': 'json decode error:' + str(res), 'rtcode': 1}
                    break
            
            if dataChk(res):
                log.debug('       dataChk true')
                break
            
            time.sleep(5)
            i = i + 1
        
        return res
    except requests.ConnectionError as e:
        return {'rtmessage': 'ConnectionError: ' + str(e), 'rtcode': 1}
    except requests.exceptions.RequestException as e:
        return {'rtmessage': 'RequestException: ' + str(e), 'rtcode': 1}

def get(group, date, resType, proxies, log_, retry=3):
    log = log_

    if date == '':
        date = date_v

    # Prepare data
    data = get_raw(group, date, resType, proxies)

    if 'stat' in data and data['stat'] == '很抱歉，沒有符合條件的資料!':
        return {'rtmessage': 'Empty Query.', 'rtcode': -1}

    if 'stat' in data and data['stat'] != 'OK':
        return {'rtmessage': 'get requests data Error :' + str(data), 'rtcode': 1}
        
    if 'rtcode' in data and data['rtcode'] != 0:
        return data

    # JSONdecode error, could be too fast, retry
    #if 'rtcode' in data and data['rtcode'] == 1:
        # XXX: Stupit retry, you will dead here
        #if retry:
            #return get(group, date, resType, retry - 1)
        #return data
    #date_v = date
    # Check have data
    if not len(data['data']):
        data['rtmessage'] = 'Empty Query.'
        data['rtcode'] = -1
        return data
    # Return multiple stock data
    runDate = data['date']
    aryData=[]
    for d in map(_format_stock_info, data['data']):
        d['date']=runDate
        aryData.append(d)
        
    data['data'] = aryData

    data['rtcode'] = 0
    #print(data['rtcode'])
    #print(data['data'])
    return data

#a = get('01','20190620','json','')