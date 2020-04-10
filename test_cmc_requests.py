import unittest as ut
from requesters import cmc_multirequests
from cmc_request import cmc_request
from log_database import db_req
from datetime import datetime


class Test_cmc_multirequest(ut.TestCase):

    def setUp(self):
        # sleep(1) # this timeout is needed to avoid throttling on the server side
        self.test_table = cmc_multirequests()
        db_req('log.db', 'CREATE TABLE IF NOT EXISTS log (id INTEGER NOT NULL PRIMARY KEY, time TEXT, table TEXT);')
        db_req('log.db', f'INSERT INTO log (time, table) values({str(datetime.now())}, {str(self.test_table)});')

    def test_time_of_response(self):
        self.time_of_response_test_passed = 0
        for item in self.test_table:
            if item[0] < 500:
                self.time_of_response_test_passed += 1
        self.assertEqual(self.time_of_response_test_passed, len(self.test_table))

    def test_actual_date(self):
        self.actual_date_test_passed = 0
        for item in self.test_table:
            if item[1]:
                self.actual_date_test_passed += 1
        self.assertEqual(self.actual_date_test_passed, len(self.test_table))

    def test_size_of_response(self):
        self.size_test_passed = 0
        for item in self.test_table:
            if item[2] < 10240:
                self.size_test_passed += 1
        self.assertEqual(self.size_test_passed, len(self.test_table))


if __name__ == '__main__':
    ut.main()
