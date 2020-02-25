import twstock
import pymongo
import time

#http://www.tej.com.tw/webtej/doc/wind1.htm
format = {'水泥工業'        :'01', '食品工業'        : '02', '塑膠工業'     :'03'
        , '紡織纖維'        :'04', '電機機械'        : '05', '電器電纜'     :'06'
        , '玻璃陶瓷'        :'08', '造紙工業'        : '09', '鋼鐵工業'     :'10'
        , '橡膠工業'        :'11', '汽車工業'        : '12', '建材營造業'   :'14'
        , '航運業'          :'15', '觀光事業'        : '16', '金融保險業'   :'17'
        , '貿易百貨業'      :'18', '綜合'            : '19', '其他業'       :'20'
        , '化學工業'        :'21', '生技醫療業'      : '22', '油電燃氣業'   :'23'
        , '半導體業'        :'24', '電腦及週邊設備業': '25', '光電業'       : '26'
        , '通信網路業'      :'27', '電子零組件業'    : '28', '電子通路業'   :'29'
        , '資訊服務業'      :'30', '其他電子業'      : '31', '文化創意業'   :'32'
        , '農業科技業'      :'33', '電子商務'        : '34', '管理股票'     :'80'
        , 'OTHER':'00'}

client = pymongo.MongoClient("mongodb://172.18.0.2:27017")
#client = pymongo.MongoClient("mongodb://192.168.1.5:27017")
db = client["twStock"] 
db.authenticate("twstock", "twstock123")
collTPEX = db["TPEX"]
collTWSE = db["TWSE"]
twstock.__update_codes()
collTPEX.delete_many({})
collTWSE.delete_many({})
"""
$group : {
    $code : {
        'type' : $type
       ,'name' : $namme
       ,'ISIN' : $ISIN
       ,'start' : $start
       ,'market' : $market
       ,'CFI' : $CFI
    }
}
"""
#取得TPEX
tpexG = {}
for k,v in twstock.tpex.items():
    groupN = ""
    if v.group == "":
        groupN = "OTHER"
    else:
        groupN = v.group
    
    data = {
             'group'  : groupN
            ,'code'   : v.code
            ,'type'   : v.type
            ,'groupCode' : format[groupN]
            ,'name'   : v.name
            ,'ISIN'   : v.ISIN
            ,'start'  : v.start
            ,'market' : v.market
            ,'CFI'    : v.CFI            
        }
    
    if groupN in tpexG:
        tpexG[groupN].update(data)
    else:
        tpexG[groupN] = data
collTPEX.insert_one(tpexG)

#取得TWSE
#twseG = {}
for k,v in twstock.twse.items():
    groupN = ""
    if v.group == "":
        groupN = "OTHER"
    else:
        groupN = v.group
        
    data = {
             'group'  : groupN
            ,'code'   : v.code
            ,'type'   : v.type
            ,'groupCode' : format[groupN]
            ,'name'   : v.name
            ,'ISIN'   : v.ISIN
            ,'start'  : v.start
            ,'market' : v.market
            ,'CFI'    : v.CFI
        }
    collTWSE.insert_one(data)
    """
    if groupN in twseG:
        twseG[groupN].update(data)
    else:
        twseG[groupN] = data
    """
#collTWSE.insert_one(twseG)
#for k,v in twstock.tpex.items():
#    print(k)
#print(twstock.tpex["1240"].type)
#v = twstock.tpex["1240"]
#print(v)