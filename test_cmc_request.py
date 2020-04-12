import unittest as ut
from datetime import datetime, timedelta
from cmc_request import cmc_request, cmc_request_mock
from settings import API_KEY, MAX_TIME_OF_RESPONSE, MAX_SIZE_OF_RESPONSE, USE_MOCK, LOG_TO_DB, UTC_OFFSET
from log_database import db_req



class TestCmcSingleRequest(ut.TestCase):
    """ This test-case checks performance of single request with designated parameters:
        Number of currencies: 10
        Sorted by volume of trade in last 24 hour.
    """

    @classmethod
    def setUpClass(cls, ) -> None:
        """Building fixture for tests"""
        if USE_MOCK:
            cls.test_tuple = cmc_request_mock()
        else:
            cls.test_tuple = cmc_request(API_KEY)
            if cls.test_tuple == None:
                raise ut.SkipTest("Invalid API-key")

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
        """ Logging results to database"""
        if LOG_TO_DB:
            db_req('log.db', "CREATE TABLE if not exists cmc_request"
                         "(id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, api_key TEXT, data TEXT, time TEXT);")
            db_req('log.db',
                    f"INSERT INTO cmc_request (api_key, data, time) values('{API_KEY}', "
                    f"'{str(datetime.now() + timedelta(hours=UTC_OFFSET))}', '{str(cls.test_tuple)}');")


if __name__ == '__main__':
    ut.main()
