import unittest as ut
from requesters import cmc_multirequests, cmc_multirequests_mock
from settings import API_KEY, USE_MOCK, LOG_TO_DB
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
        """ Test if time of response less than 500 msec
        """
        self.time_of_response_test_passed = 0
        for item in self.test_table:
            if item[0] < 500:
                self.time_of_response_test_passed += 1
        self.assertEqual(self.time_of_response_test_passed, len(self.test_table)),

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
