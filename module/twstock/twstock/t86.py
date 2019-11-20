import datetime
import json
import time
import requests
import twstock
import sys
#http://www.twse.com.tw/fund/T86?response=json&date=20190528&selectType=01&_=1559145215220
#https://godoc.org/github.com/toomore/gogrs/twse go的方式取股票
STOCKINFO_URL = 'http://www.twse.com.tw/fund/T86'
global date_v
date_v = datetime.datetime.now().strftime("%Y%m%d")

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
    result['FII_I'] = data[2] + data[5]
    result['FII_O'] = data[3] + data[6]
    result['SIT_I'] = data[8]
    result['SIT_O'] = data[9]
    result['DProp_I'] = data[12]
    result['DProp_O'] = data[13]
    result['DHedge_I'] = data[15]
    result['DHedge_O'] = data[16]
    
    return result

def dataChk(res):
    if 'stat' in res and res['stat'] == 'OK':
        datalist = res['data']
        for d in datalist:
            if len(d) != 18:
                return False
    return True

def get_raw(group, date, resType, proxies) -> dict:
    try:
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
            if 'http' in proxies:
                req.get(STOCKINFO_URL, proxies=proxies)
            else:
                req.get(STOCKINFO_URL)
            t=int(time.time()) * 1000
            p = {'response': resType, 'date': date, 'selectType':group, '_':t}
            if 'http' in proxies:
                res = req.get(STOCKINFO_URL, proxies=proxies, params=p)
            else:
                res = req.get(STOCKINFO_URL, params=p)
            print(str(res.json))
            if sys.version_info < (3, 5):
                try:
                    res = res.json()
                except ValueError:
                    res = {'rtmessage': 'json decode error:' + str(res), 'rtcode': 1}
                    break
            else:
                try:
                    res = res.json()
                except json.decoder.JSONDecodeError:
                    res = {'rtmessage': 'json decode error:' + str(res), 'rtcode': 1}
                    break
            
            if 'status_code' in res and res.status_code != 200:
                res = {'rtmessage': str(res.status_code), 'rtcode': 1}
                break
            
            if dataChk(res):
                break
            i = i + 1
        
        return res
    except requests.ConnectionError as e:
        return {'rtmessage': 'ConnectionError: ' + str(e), 'rtcode': 1}

def get(group, date, resType, proxies, retry=3):
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