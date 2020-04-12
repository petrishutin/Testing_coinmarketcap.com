"""
This is testing module for task. The task is to test performance of https://coinmarketcap.com/ API
The task is divided in two stages.

1 Stage.
Define a function sending request to API returning data for 10 currencies with greatest volume in last 24 hours
DONE: in module cmc_request.py, function - cmc_requests()

Test function if:
    - time of response is less than MAX_TIME_OF_RESPONSE. 500 msec by task
    - latest update date for each currency in each thread is matching local current date
    - size of response is less than MAX_SIZE_OF_RESPONSE. 10kb by task
DONE: in module test_cmc_requests.py

2 Stage:
Run request in several threads.
DONE: In module cmc_multirequest.py function cmc_multirequests.
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
from datetime import datetime, timedelta
from cmc_multirequest import cmc_multirequest, cmc_multirequest_mock
from settings import USE_MOCK, LOG_TO_DB, MAX_PERCENTILE, MAX_TIME_OF_RESPONSE, \
    MIN_RPS, MAX_SIZE_OF_RESPONSE, UTC_OFFSET, API_KEY
from log_database import db_req


class TestCmcMultirequest(ut.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """Building fixture for tests"""
        if USE_MOCK:
            cls.test_table = cmc_multirequest_mock()
        else:
            cls.test_table = cmc_multirequest()
            for item in cls.test_table:
                if not item:
                    raise ut.SkipTest("Invalid API-key")

    def test_stage1_time_of_response(self):
        """ Testing if time of response in each thread is less than 500 msec by task"""
        self.time_of_response_test_passed = 0
        for item in self.test_table:
            if item[0] < MAX_TIME_OF_RESPONSE:
                self.time_of_response_test_passed += 1
        self.assertEqual(self.time_of_response_test_passed, len(self.test_table)), str(self.test_table)

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
        """ Logging results to database"""
        if LOG_TO_DB:
            db_req('log.db', "CREATE TABLE if not exists cmc_multirequest"
                             "(id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, api_key TEXT, data TEXT, time TEXT);")
            db_req('log.db',
                   f"INSERT INTO cmc_multirequest (api_key, data, time) values('{API_KEY}', "
                   f"'{str(datetime.now() + timedelta(hours=UTC_OFFSET))}', '{str(cls.test_table)}');")


if __name__ == '__main__':
    ut.main()
