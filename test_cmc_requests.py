"""
This is testing module for task. The task is to test performance of https://coinmarketcap.com/ API
The task is divided in two stages.

1 Stage.
Define a function sending request to API returning data for 10 currencies with greatest volume in last 24 hours
DONE: in module cmc_request.py, function - cmc_requests()

Test API-response if:
    - time of response is less than 500 msec by task
    - latest update date for each currency in is matching local current date
    - size of response is less than 10kb by task
DONE: TestCase - TestCmcSingleRequest

2 Stage:
Run request in several threads.
DONE: cmc_multirequest_fixture
Check tests of stage 1 for each thread
DONE: In test_cmc_multirequest.py in:
    - test_stage1_time_of_response()
    - test_stage1_actual_date()
    - test_stage1_size_of_response()
Check if 80% latency less than 450 msec by task
DONE: - test_stage2_percentile()
Check if rps (response per second) is greater than 5
DONE: - test_stage2_rps()

Type $: cricket-unittest in terminal to run all test modules with nice UI
"""

import unittest as ut
import numpy as np
import json
from threading import Thread
from time import time
from datetime import datetime, timedelta
from cmc_request import cmc_request

API_KEY: str = '7254bf31-94e2-412a-9698-be3d82bca351'  # get the key at https://coinmarketcap.com/api/
UTC_OFFSET: int = 3  # Set UTC offset in hours for your current location
LOG: bool = True
NUMBER_OF_TREADS: int = 8

# test limits
MAX_PERCENTILE: int = 450  # Upper limit of 80% latency in msec
MAX_TIME_OF_RESPONSE: int = 500  # Upper limit for time of response in msec
MIN_RPS: int = 5  # Lower limit of rps (responses per second)
MAX_SIZE_OF_RESPONSE: int = 10240  # Upper limit for size of response in bytes


def cmc_request_fixture(api_key: str = API_KEY) -> tuple:
    t1 = time()
    response = cmc_request(API_KEY)
    t2 = time()
    if not response:
        return tuple()
    time_of_response = int((t2 - t1) * 1000)
    data = json.loads(response.text)
    try:
        currencies_data = list(data['data'])
    except KeyError:
        return tuple()
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
    size_of_responce: int = len(response.content)
    if LOG:
        with open('log_cmc_requests.csv', 'a') as log:
            log.write(f"{API_KEY}, {str(datetime.now() - timedelta(hours=UTC_OFFSET))},"
                      f"{time_of_response, actual_date, size_of_responce} \n")
    return time_of_response, actual_date, size_of_responce,


class TestCmcSingleRequest(ut.TestCase):
    """ This test-case checks performance of single request with designated parameters:
        Number of currencies: 10
        Sorted by volume of trade in last 24 hour.
    """

    @classmethod
    def setUpClass(cls, ) -> None:
        """fixture for tests"""
        cls.test_tuple = cmc_request_fixture()
        if not cls.test_tuple:  # Check if test array is not empty. So API-key is valid and connection available
            raise ut.SkipTest("Check API-key and If https://coinmarketcap.com/ is available")

    def test_time_of_response(self):
        """ Checking, If time of response is less than 500 msec by task"""
        self.assertLess(self.test_tuple[0], MAX_TIME_OF_RESPONSE)

    def test_actual_date(self):
        """Checking if update date in response matching current date"""
        self.assertTrue(self.test_tuple[1])

    def test_size_of_resonse(self):
        """Checking in size of response is less than 10Kb by task"""
        self.assertLess(self.test_tuple[2], MAX_SIZE_OF_RESPONSE)

    @classmethod
    def tearDownClass(cls) -> None:
        pass


class Requester(Thread):
    """Class for running cmc_requests in multithreads and save results of all threads"""
    report_list = []

    def __init__(self, api_key):
        super(Requester, self).__init__(target=self.job, args=tuple())
        self.api_key = api_key
        self.start()

    def job(self):
        self.response = cmc_request_fixture(self.api_key)
        Requester.report_list.append(self.response)


def cmc_multirequest_fixture() -> list:
    """ Runs cmc_request in several threads.
        Number of threads can be adjusted by setting value of NUMBER_OF_TREADS,
    """
    list_of_threads = []  # defining list for pool of threads
    for thr in range(NUMBER_OF_TREADS):  # building the pool
        list_of_threads.append(Requester(API_KEY))  # appending thread to pool
    while list_of_threads:  # Checking if any thread in pool is alive
        for thread in list_of_threads:
            if not thread.is_alive():
                list_of_threads.remove(thread)
    # When all threads are dead returning
    return Requester.report_list


class TestCmcMultiRequest(ut.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """fixture for tests cmc multithread request"""
        cls.test_table = cmc_multirequest_fixture()
        for item in cls.test_table:
            if not item:
                raise ut.SkipTest("Check API-key and If https://coinmarketcap.com/ is available")

    def test_stage1_time_of_response(self):
        """ Testing if time of response in each thread is less than 500 msec by task"""
        self.time_of_response_test_passed = 0
        for item in self.test_table:
            if item[0] < MAX_TIME_OF_RESPONSE:
                self.time_of_response_test_passed += 1
        self.assertEqual(self.time_of_response_test_passed, len(self.test_table))

    def test_stage1_actual_date(self):
        """Testing if date of update in response of each thread is matching current date in current location"""
        self.actual_date_test_passed = 0
        for item in self.test_table:
            if item[1]:
                self.actual_date_test_passed += 1
        self.assertEqual(self.actual_date_test_passed, len(self.test_table))

    def test_stage1_size_of_response(self):
        """Testing if size of response in each thread is less than 10Kb"""
        self.size_test_passed = 0
        for item in self.test_table:
            if item[2] < MAX_SIZE_OF_RESPONSE:
                self.size_test_passed += 1
        self.assertEqual(self.size_test_passed, len(self.test_table))

    def test_stage2_percentile(self):
        """ Testing if 80% percentile is less than  450 msec among all threads"""
        list_of_timings = []
        for item in self.test_table:
            list_of_timings.append(item[0])
        arr = np.array(list_of_timings)
        percent = np.percentile(arr, 80)
        self.assertLess(percent, MAX_PERCENTILE)

    def test_stage2_rps(self):
        """Test if rps (response per second) is greater than 5"""
        list_of_timings = []
        for item in self.test_table:
            list_of_timings.append(item[0])
        last_thread_finnished = min(list_of_timings) / 1000
        rps = len(self.test_table) / last_thread_finnished
        self.assertGreater(rps, MIN_RPS)

    @classmethod
    def tearDownClass(cls) -> None:
        pass


if __name__ == '__main__':
    ut.main()
