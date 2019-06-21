import requests
import twstock
#http://www.twse.com.tw/fund/T86?response=json&date=20190528&selectType=01&_=1559145215220
STOCKINFO_URL = 'http://www.twse.com.tw/fund/T86'

req = requests.Session()
req.get(STOCKINFO_URL)
p = {'response': 'json', 'date': '20190501', 'selectType':'01', '_':int(time.time()) * 1000))}
r = req.get(STOCKINFO_URL, params=p)
print(r.url)
print(r.json)