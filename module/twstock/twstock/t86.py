import datetime
import json
import time
import requests
import twstock
#http://www.twse.com.tw/fund/T86?response=json&date=20190528&selectType=01&_=1559145215220
#https://godoc.org/github.com/toomore/gogrs/twse go的方式取股票
STOCKINFO_URL = 'http://www.twse.com.tw/fund/T86'
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
    
    try:
        result['code'] = data[0]
        result['date'] = date_v
        result['FII_I'] = data[2] + data[5]
        result['FII_O'] = data[3] + data[6]
        result['SIT_I'] = data[8]
        result['SIT_O'] = data[9]
        result['DProp_I'] = data[12]
        result['DProp_O'] = data[13]
        result['DHedge_I'] = data[15]
        result['DHedge_O'] = data[16]
    
        # Success fetching
        result['rtcode'] = 0
    except:
        result['rtcode'] = -1
        
    return result

def get_raw(group, date, resType) -> dict:
    try:
        req = requests.Session()
        req.get(STOCKINFO_URL)
        time=int(time.time()) * 1000
        p = {'response': resType, 'date': date, 'selectType':group, '_':time}
        r = req.get(STOCKINFO_URL, params=p)
        if r.stat != 'OK':
            return {'rtmessage': 'get requests data Error', 'rtcode': 1}
        
        if sys.version_info < (3, 5):
            try:
                return r.json()
            except ValueError:
                return {'rtmessage': 'json decode error', 'rtcode': 1}
        else:
            try:
                return r.json()
            except json.decoder.JSONDecodeError:
                return {'rtmessage': 'json decode error', 'rtcode': 1}
    except requests.ConnectionError:
        return {'rtmessage': 'ConnectionError', 'rtcode': 1}

def get(group, date, resType, retry=3):
    if date == '':
        date = date_v

    # Prepare data
    data = get_raw(group, date, resType)

    # JSONdecode error, could be too fast, retry
    if data['rtcode'] == 1:
        # XXX: Stupit retry, you will dead here
        if retry:
            return get(group, date, resType, retry - 1)
        return data
    date_v = date
    # Check have data
    if not len(data['data']):
        data['rtmessage'] = 'Empty Query.'
        data['rtcode'] = -1
        return data
    # Return multiple stock data
    data = [v for d in map(_format_stock_info, data['data'])]

    data['rtcode'] = 0
    print(data)
    return data

    
    
