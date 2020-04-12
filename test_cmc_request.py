import unittest as ut
from cmc_request import cmc_request, cmc_request_mock
from settings import API_KEY, MAX_TIME_OF_RESPONSE, MAX_SIZE_OF_RESPONSE, USE_MOCK


class TestCmcSingleRequestPerfomance(ut.TestCase):
    """ This test-case checks performance of single request with designated parameters:
        Number of currencies: 10
        Sorted by volume of trade in last 24 hour.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Building fixture for tests"""
        cls.invalid_api_key = False
        if USE_MOCK:
            cls.test_tuple = cmc_request_mock()
        else:
            try:
                cls.test_tuple = cmc_request(API_KEY)
            except KeyError:
                cls.invalid_api_key = True
    # @ut.skiped
    def test_time_of_response(self):
        """ Checking, If time of response is less than MAX_TIME_OF_RESPONSE. 500 msec by task"""
        if self.invalid_api_key:
            raise KeyError("Invalid Api-key")
        self.assertLess(self.test_tuple[0], MAX_TIME_OF_RESPONSE)

    # @ut.skiped
    def test_actual_date(self):
        """Checking if update date in response matching current date"""
        if self.invalid_api_key:
            raise KeyError("Invalid Api-key")
        self.assertTrue(self.test_tuple[1])

    # @ut.skiped
    def test_size_of_resonse(self):
        """Checking in size of response is less than MAX_SIZE_OF_RESPONSE. 10Kb by task"""
        if self.invalid_api_key:
            raise KeyError("Invalid Api-key")
        self.assertLess(self.test_tuple[2], MAX_SIZE_OF_RESPONSE)


if __name__ == '__main__':
    ut.main()
