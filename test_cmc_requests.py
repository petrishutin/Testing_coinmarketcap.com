import unittest as ut
import numpy as np
from Requesters import cmc_multirequests, cmc_multirequests_mock
from settings import USE_MOCK, LOG_TO_DB, MAX_PERCENTILE, MAX_TIME_OF_RESPONSE, MIN_RPS, MAX_SIZE_OF_RESPONSE
from log_database import db_req
from datetime import datetime


class Test_cmc_multirequest(ut.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if USE_MOCK:
            cls.test_table = cmc_multirequests_mock()
        else:
            cls.test_table = cmc_multirequests()
        if LOG_TO_DB:
            db_req('log.db', "CREATE TABLE if not exists log "
                             "(id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, data TEXT, time TEXT);")
            db_req('log.db', f"INSERT INTO log (data, time) values('{str(datetime.now())}', '{str(cls.test_table)}');")

    def test_time_of_response(self):
        """ Test if time of response in each thread is less than 500 msec"""
        self.time_of_response_test_passed = 0
        for item in self.test_table:
            if item[0] < MAX_TIME_OF_RESPONSE:
                self.time_of_response_test_passed += 1
        self.assertEqual(self.time_of_response_test_passed, len(self.test_table)), str(self.test_table)

    def test_actual_date(self):
        """Test if date of update in response of each thread is matching current date in current location"""
        self.actual_date_test_passed = 0
        for item in self.test_table:
            if item[1]:
                self.actual_date_test_passed += 1
        self.assertEqual(self.actual_date_test_passed, len(self.test_table))

    def test_size_of_response(self):
        """Testing if size of response in each thread is less than 10Kb"""
        self.size_test_passed = 0
        for item in self.test_table:
            if item[2] < MAX_SIZE_OF_RESPONSE:
                self.size_test_passed += 1
        self.assertEqual(self.size_test_passed, len(self.test_table))

    def test_percentile(self):
        """ Testing if 80% percentile is less than 450 msec among all threads"""
        l = []
        for item in self.test_table:
            l.append(item[0])
        arr = np.array(l)
        percent = np.percentile(arr, 80)
        self.assertLess(percent, MAX_PERCENTILE)

    def test_rps(self):
        """Test if rps (response per second) is greater than 5"""
        l = []
        for item in self.test_table:
            l.append(item[0])
        last_thread_finnished = min(l) / 1000
        rps = len(self.test_table) / last_thread_finnished
        self.assertGreater(rps, MIN_RPS)


if __name__ == '__main__':
    ut.main()
