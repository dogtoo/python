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
#https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=20191127&type=ALLBUT0999&_=1574859382270 個股 data9

#https://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&se=02&t=D&d=109/03/20&_=1584706885077 t86
#https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d=109/03/19&_=1584706711888 stockDay

#global date_v
#date_v = datetime.datetime.now().strftime("%Y%m%d")
log = logging
def _format_stock_info(data) -> dict:
    result = {
        'code': '' # 0
      , 'date': '' # reportDate
      , 'FII_I': 0 #外資買進
      , 'FII_O': 0 #外資賣出
      , 'SIT_I': 0 #投信買進
      , 'SIT_O': 0 #投信賣出
      , 'DProp_I': 0 #自營商(自行買賣)
      , 'DProp_O': 0 #自營商(自行買賣)
      , 'DHedge_I': 0 #自營商(避險)
      , 'DHedge_O': 0 #自營商(避險)
      , 'Stock_Type': ''
    }
    
    result['code'] = data[0]
    result['date'] = ''
    result['Stock_Type'] = 'tes'
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
    
def _format_stock_info_tpex(data) -> dict:
    result = {
        'code': '' # 0
      , 'date': '' # reportDate
      , 'FII_I': 0 #外資買進 2
      , 'FII_O': 0 #外資賣出 3
      , 'SIT_I': 0 #投信買進 11
      , 'SIT_O': 0 #投信賣出 12
      , 'DProp_I': 0 #自營商(自行買賣) 17
      , 'DProp_O': 0 #自營商(自行買賣) 18
      , 'DHedge_I': 0 #自營商(避險) 20
      , 'DHedge_O': 0 #自營商(避險) 21
      , 'Stock_Type': ''
    }
    
    result['code'] = data[0]
    result['date'] = ''
    result['Stock_Type'] = 'otc'
    if len(data) == 11:
        result['FII_I'] = int(data[2].replace(',',''))
        result['FII_O'] = int(data[3].replace(',',''))
        result['SIT_I'] = int(data[5].replace(',',''))
        result['SIT_O'] = int(data[6].replace(',',''))
        result['DProp_I'] = int(data[8].replace(',',''))
        result['DProp_O'] = int(data[9].replace(',',''))
        result['DHedge_I'] = 0
        result['DHedge_O'] = 0
    elif len(data) == 25:
        result['FII_I'] = int(data[2].replace(',',''))
        result['FII_O'] = int(data[3].replace(',',''))
        result['SIT_I'] = int(data[11].replace(',',''))
        result['SIT_O'] = int(data[12].replace(',',''))
        result['DProp_I'] = int(data[17].replace(',',''))
        result['DProp_O'] = int(data[18].replace(',',''))
        result['DHedge_I'] = int(data[20].replace(',',''))
        result['DHedge_O'] = int(data[21].replace(',',''))
    
    return result

def _format_stock_day_info(data) -> dict:
    result = {
        'code': ''
      , 'date': ''
      , 'Trade_Volume': 0 #成交股數
      , 'Transaction': 0 #成交筆數
      , 'Trade_Value': 0 #成交金額
      , 'Opening_Price': 0 #開盤價
      , 'Highest_Price': 0 #最高價
      , 'Lowest_Price': 0 #最低價
      , 'Closing_Price': 0 #收盤價
      , 'Change': 0 #漲跌差價
      , 'Last_Best_Bid_Price': 0#最後揭示買價
      , 'Last_Best_Bid_Volume': 0#最後揭示買量 
      , 'Last_Best_Ask_Price': 0#最後揭示賣價
      , 'Last_Best_Ask_Volume': 0#最後揭示賣量
      , 'Price_Earning_Ratio': 0#本益比
      , 'Stock_Type': ''
    }

    result['code'] = data[0]
    result['date'] = ''
    try:
        result['Stock_Type'] = 'tes'
        result['Trade_Volume'] = int(data[2].replace(',',''))
        result['Transaction'] = int(data[3].replace(',',''))
        result['Trade_Value'] = int(data[4].replace(',',''))
        if data[5].replace(' ','') != '--':
            result['Opening_Price'] = float(data[5].replace(',',''))
            result['Highest_Price'] = float(data[6].replace(',',''))
            result['Lowest_Price'] = float(data[7].replace(',',''))
            result['Closing_Price'] = float(data[8].replace(',',''))
            if result['Closing_Price'] >= result['Opening_Price']:
                result['Change'] = float(data[10].replace(',',''))
            else:
                result['Change'] = -float(data[10].replace(',',''))
        
        if data[11].replace(' ','') != '--':
            result['Last_Best_Bid_Price'] = float(data[11].replace(',',''))
        
        if data[13].replace(' ','') != '--':
            result['Last_Best_Ask_Price'] = float(data[13].replace(',',''))
        
        result['Price_Earning_Ratio'] = float(data[15].replace(',',''))
        
        result['Last_Best_Bid_Volume'] = int(data[12].replace(',',''))
        result['Last_Best_Ask_Volume'] = int(data[14].replace(',',''))
    except BaseException as e:
        logging.info("停牌可能 = " + str(data))
    return result

def _format_stock_day_info_tpex(data) -> dict:
    result = {
        'code': ''
      , 'date': ''
      , 'Trade_Volume': 0 #成交股數 8
      , 'Transaction': 0 #成交筆數 10
      , 'Trade_Value': 0 #成交金額 9
      , 'Opening_Price': 0 #開盤價 4
      , 'Highest_Price': 0 #最高價 5
      , 'Lowest_Price': 0 #最低價 6
      , 'Closing_Price': 0 #收盤價 2
      , 'Change': 0 #漲跌差價 3
      , 'Last_Best_Bid_Price': 0#最後揭示買價 11
      , 'Last_Best_Bid_Volume': 0#最後揭示買量 
      , 'Last_Best_Ask_Price': 0#最後揭示賣價 12
      , 'Last_Best_Ask_Volume': 0#最後揭示賣量
      , 'Price_Earning_Ratio': 0#本益比
      , 'Stock_Type': ''
    }

    result['code'] = data[0]
    result['date'] = ''
    try:
        result['Stock_Type'] = 'otc'
        result['Trade_Volume'] = int(data[8].replace(',',''))
        result['Transaction'] = int(data[10].replace(',',''))
        result['Trade_Value'] = int(data[9].replace(',',''))
        if data[4].replace(' ','') != '---':
            result['Opening_Price'] = float(data[4].replace(',',''))
            result['Highest_Price'] = float(data[5].replace(',',''))
            result['Lowest_Price'] = float(data[6].replace(',',''))
            result['Closing_Price'] = float(data[2].replace(',',''))
            result['Change'] = float(data[3].replace(',',''))
            #if result['Closing_Price'] >= result['Opening_Price']:
            #    result['Change'] = float(data[3].replace(',',''))
            #else:
            #    result['Change'] = -float(data[3].replace(',',''))
        
        if data[11].replace(' ','') != '---':
            result['Last_Best_Bid_Price'] = float(data[11].replace(',',''))
        
        if data[12].replace(' ','') != '---':
            result['Last_Best_Ask_Price'] = float(data[12].replace(',',''))
        
        #result['Price_Earning_Ratio'] = float(data[15].replace(',',''))
        
        #result['Last_Best_Bid_Volume'] = int(data[12].replace(',',''))
        #result['Last_Best_Ask_Volume'] = int(data[14].replace(',',''))
    except BaseException as e:
        logging.info("停牌可能 = " + str(data))
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

def dateFormat(date):
    d_ = str(int(date) - 19110000)
    logging.debug(d_[0:3] + '/' + d_[3:5] + '/' + d_[5:7])
    return d_[0:3] + '/' + d_[3:5] + '/' + d_[5:7]

#def get_raw(group, date, resType, proxies) -> dict:
def get_raw(group, date, resType, proxies, source) -> dict:
    try:
        if source == 't86':
            if int(date) < 20120501:
                STOCKINFO_URL = 'https://www.twse.com.tw/fund/TWT47U'
            else:
                STOCKINFO_URL = 'http://www.twse.com.tw/fund/T86'
            p = {'response': resType, 'date': date, 'selectType':group}
        elif source == 'stockDay':
            STOCKINFO_URL = 'https://www.twse.com.tw/exchangeReport/MI_INDEX'
            p = {'response': resType, 'date': date, 'type':group}
        elif source == 'tpex86': #begin 20070421
            if int(date) <= 20061231:
                STOCKINFO_URL = 'https://hist.tpex.org.tw/hist/STOCK/3INSTI/DAILY_TRADE/' #BIGD951229S_N.html html格式，要再轉
            elif int(date) <= 20070420:
                STOCKINFO_URL = 'https://www.tpex.org.tw/storage/zh-tw/web/stock/3insti/daily_trade/3itradeHis.htm' #抓不到資料
            elif int(date) <= 20141130:
                STOCKINFO_URL = 'https://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_result.php' #L = 11
            elif int(date) > 20141130:
                STOCKINFO_URL = 'https://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php' #L = 24
            p = {'l':'zh-tw', 't':'D', 'd': dateFormat(date), 'se':group}
        elif source == 'tpexDay': #begin 20070101
            if int(date) <= 20061231: # begin 20030801
                STOCKINFO_URL = 'https://hist.tpex.org.tw/hist/STOCK/AFTERTRADING/DAILY_CLOSE_QUOTES/' #RSTA3104_951228.HTML html格式，要再轉
            if int(date) <= 20070420:
                STOCKINFO_URL = 'https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotesB/stk_quote.php'
                p = {'ajax':'true', 'input_date': dateFormat(date)} #html格式，要再轉
            elif int(date) > 20070420:
                STOCKINFO_URL = 'https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php'
                p = {'l':'zh-tw', 'd': dateFormat(date)}
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
            #p = {'response': resType, 'date': date, 'selectType':group, '_':t}
            p['_'] = t
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
            
            #if dataChk(res):
            if source == 't86' and dataChk(res):
                log.debug('       dataChk true')
                break
            else:
                break
            
            time.sleep(5)
            i = i + 1
        
        return res
    except requests.ConnectionError as e:
        return {'rtmessage': 'ConnectionError: ' + str(e), 'rtcode': 1}
    except requests.exceptions.RequestException as e:
        return {'rtmessage': 'RequestException: ' + str(e), 'rtcode': 1}

def get(group, date, resType, proxies, source, log_, retry=3):
    log = log_
    if date == '':
        #date = date_v
        date = datetime.datetime.now().strftime("%Y%m%d")
    s_ = 'tp'
    if source == 't86' or source == 'stockDay':
        s_ = 'tw'            

    # Prepare data
    data = get_raw(group, date, resType, proxies, source)
    logging.debug('stock_type:' + s_)
    aryData=[]
    if s_ == 'tw':
        if 'stat' in data and data['stat'] == '很抱歉，沒有符合條件的資料!':
            return {'rtmessage': 'Empty Query.', 'rtcode': -1}

        if 'stat' in data and data['stat'] != 'OK':
            return {'rtmessage': 'get requests data Error :' + str(data), 'rtcode': 1}
            
        if 'rtcode' in data and data['rtcode'] != 0:
            return data

        if source == 't86':
            # Check have data
            if not len(data['data']):
                data['rtmessage'] = 'Empty Query.'
                data['rtcode'] = -1
                return data
            # Return multiple stock data
            runDate = data['date']
            
            for d in map(_format_stock_info, data['data']):
                d['date']=runDate
                aryData.append(d)
        elif source == 'stockDay':
            # Return multiple stock data
            runData = []
            if int(date) < 20110801:
                runData = data['data8']
            else:
                runData = data['data9']
            
            if not len(runData):
                data['rtmessage'] = 'Empty Query.'
                data['rtcode'] = -1
                return data
            
            for d in map(_format_stock_day_info, runData):
                d['date']=date
                aryData.append(d)
            
        data['data'] = aryData
        data['rtcode'] = 0
    else:
        if not len(data['aaData']):
            data['rtmessage'] = 'Empty Query.'
            data['rtcode'] = -1
            return data
        runData = data['aaData']
        logging.debug(runData)
        if source == 'tpex86':
            for d in map(_format_stock_info_tpex, runData):
                d['date']=date
                aryData.append(d)
        elif source == 'tpexDay':
            for d in map(_format_stock_day_info_tpex, runData):
                d['date']=date
                logging.debug(d)
                aryData.append(d)

        data['data'] = aryData
        data['rtcode'] = 0
    #print(data['rtcode'])
    #print(data['data'])
    return data

#a = get('01','20190620','json','')

def StockChk(res):
    if 'stat' in res and res['stat'] == 'OK':
        datalist = []
        if int(res['date']) < 20110801:
            datalist = res['data8']
        else:
            datalist = res['data9']
        for d in datalist:
            #log.debug('       len = ' + str(len(d)))
            if len(d) != 16:
                log.error('       len = ' + str(len(d)))
                return False
    return True

#def get_STOCK_DAY(group, date, resType, proxies) -> dict:
#    try:
#        STOCKINFO_URL = 'https://www.twse.com.tw/exchangeReport/MI_INDEX'
#
#        i = 0
#        res = {'rtmessage': 'get error', 'rtcode': 1}
#        while i < 10:
#            req = requests
#            
#            t=int(time.time()) * 1000
#            p = {'response': resType, 'date': date, 'type':group, '_':t}
#                
#            if 'http' in proxies:
#                log.debug('       proxy get data begin')
#                res = req.get(STOCKINFO_URL, proxies=proxies, params=p, timeout=(5, 80))
#                log.debug('       proxy get data end')
#            else:
#                log.debug('       get data begin')
#                res = req.get(STOCKINFO_URL, params=p, timeout=(5, 80))
#                log.debug('       get data end')
#            
#            if 'status_code' in res and res.status_code != 200:
#                res = {'rtmessage': str(res.status_code), 'rtcode': 1}
#                break
#            
#            if sys.version_info < (3, 5):
#                try:
#                    res = res.json()
#                    log.debug('       res.json')
#                except ValueError:
#                    res = {'rtmessage': 'json decode error:' + str(res), 'rtcode': 1}
#                    break
#            else:
#                try:
#                    res = res.json()
#                    log.debug('       res.json')
#                except json.decoder.JSONDecodeError:
#                    res = {'rtmessage': 'json decode error:' + str(res), 'rtcode': 1}
#                    break
#            
#            if StockChk(res):
#                log.debug('       dataChk true')
#                break
#            
#            time.sleep(5)
#            i = i + 1
#        
#        return res
#    except requests.ConnectionError as e:
#        return {'rtmessage': 'ConnectionError: ' + str(e), 'rtcode': 1}
#    except requests.exceptions.RequestException as e:
#        return {'rtmessage': 'RequestException: ' + str(e), 'rtcode': 1}

def STOCK_DAY(group, date, resType, proxies, log_, retry=3):
    log = log_

    if date == '':
        date = date_v

    # Prepare data
    data = get_STOCK_DAY(group, date, resType, proxies)

    if 'stat' in data and data['stat'] == '很抱歉，沒有符合條件的資料!':
        return {'rtmessage': 'Empty Query.', 'rtcode': -1}

    if 'stat' in data and data['stat'] != 'OK':
        return {'rtmessage': 'get requests data Error :' + str(data), 'rtcode': 1}
        
    if 'rtcode' in data and data['rtcode'] != 0:
        return data
        
    # Return multiple stock data
    runData = []
    if int(date) < 20110801:
        runData = data['data8']
    else:
        runData = data['data9']
    
    if not len(runData):
        data['rtmessage'] = 'Empty Query.'
        data['rtcode'] = -1
        return data
    
    aryData=[]
    for d in map(_format_stock_day_info, runData):
        d['date']=date
        aryData.append(d)
        
    data['data'] = aryData

    data['rtcode'] = 0
    #print(data['rtcode'])
    #print(data['data'])
    return data