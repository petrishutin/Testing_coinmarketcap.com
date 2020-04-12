"""
This module defines function to request coinmarketcap API with designated parameters.
Number of currencies: 10
Sorted by valume of trade in last 24 hour
These functions are needed to get performance values and validate it in test module.

Also cmc_request checks if dates in response is matching local current date.
Use UTC_OFFSET to set current timezone.
"""

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
from datetime import datetime, timedelta
from settings import API_KEY, UTC_OFFSET


def cmc_request(api_key: str) -> tuple:
    """ Function receives API key and sends request to coinmarketcap API designated parameters:
        Namber of currencies: 10
        Sorted by valume of trade in last 24 hour
        Returns tuple with:
            - Integer. time of response (in msec)
            - Boolean value. True if date of last update matching local date
            - Integer. size of response in bytes
    """
    assert isinstance(api_key, str), 'API-key must be a string'
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '10',
        'convert': 'USD',
        'sort': 'volume_24h'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
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
    try:
        currencies_data = list(data['data'])
    except KeyError:
        return

    actual_date_count = 0
    actual_date: bool = False
    # Cheking if update date for each coins is matching current date
    for item in currencies_data:
        update_time_utc = item['quote']['USD']['last_updated']
        # brinning UTC date of response to local time with UTC_OFFSET
        update_time_local = datetime.strptime(update_time_utc, '%Y-%m-%dT%H:%M:%S.000Z') + timedelta(hours=UTC_OFFSET)
        update_date = datetime.timetuple(update_time_local)[:3]
        current_date = datetime.timetuple(datetime.today())[:3]
        if update_date == current_date:
            actual_date_count += 1
    if actual_date_count == len(currencies_data):
        actual_date = True
    time_of_responce: int = int((t2 - t1) * 1000)  # returns time in msec
    size_of_responce: int = len(response.content)
    return time_of_responce, actual_date, size_of_responce,

def cmc_request_mock() -> tuple:
    """Returns mock data with same format as cmc_request"""
    return 300, True, 10000,

if __name__ == '__main__':
    print(cmc_request(API_KEY))
