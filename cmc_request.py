"""
This module defines function to request coinmarketcap API with designated parameters.
Number of currencies: 10
Sorted by valume of trade in last 24 hour
"""

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from pprint import pprint

def cmc_request(api_key: str) -> 'response in json':
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
        response = session.request('get', url, parameters)
        return response
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return None
    finally:
        session.close()


if __name__ == '__main__':
    API_KEY: str = '7254bf31-94e2-412a-9698-be3d82bca351'  # get the kay at https://coinmarketcap.com/api/
    pprint(cmc_request(API_KEY))

