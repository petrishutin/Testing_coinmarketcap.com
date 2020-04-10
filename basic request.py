from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
from pprint import pprint

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start':'1',
    'limit':'10',
    'convert':'USD',
    'sort':'volume_24h'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '983491f0-fa9c-49ff-b88b-0694b4e99109',
}

session = Session()
session.headers.update(headers)

try:
    t1 = time.time()
    response = session.get(url, params=parameters)
    t2 = time.time()
    data = json.loads(response.text)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
data = list(data['data'])
num = 1
for item in data:
    print(num, '|',item['id'], '|', item['name'], '|', item['quote']['USD']['volume_24h'])
    num += 1

pprint(data)
print('size', len(response.content))
print('time', t2-t1)
