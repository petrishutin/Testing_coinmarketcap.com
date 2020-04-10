"""
This module defines function to request coinmarketcap API with designated parameters.
These functions are needed to get performance values and validate it in test modile.
"""

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
from datetime import datetime, timedelta
from settings import API_KEY


def cmc_request(api_key: str) -> tuple:
    """ Function receives API key and sends request to coinmarketcap API designated parameters:
        Namber of currencies: 10
        Sorted by valume of trade in last 24 hour
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
    data = list(data['data'])

    actual_date_count = 0
    actual_date = False
    # Cheking if update date for each coins is matching current date
    for item in data:
        update_time_utc = item['quote']['USD']['last_updated']
        # brinning UTC date of response to local time (UTC +3)
        update_time_local = datetime.strptime(update_time_utc, '%Y-%m-%dT%H:%M:%S.000Z') + timedelta(hours=3)
        update_date = datetime.timetuple(update_time_local)[:3]
        current_date = datetime.timetuple(datetime.today())[:3]
        if update_date == current_date:
            actual_date_count += 1
    if actual_date_count == len(data):
        actual_date = True
    time_of_responce = (t2 - t1) * 1000  # returns time in msec
    size_of_responce = len(response.content)
    return time_of_responce, actual_date, size_of_responce,


if __name__ == '__main__':
    print(cmc_request(API_KEY))
