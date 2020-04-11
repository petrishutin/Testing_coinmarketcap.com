""" This module runs cmc_request in several threads.
    Number of threads can be set in settings.py file as NUMBER_OF_TREADS
    Also module contains cmc_multirequests_mock function.
    If USE_MOCK is set to True all tests will be run with mock fixture.
"""

from threading import Thread
from pprint import pprint
from cmc_request import cmc_request
from settings import API_KEY, NUMBER_OF_TREADS, USE_MOCK


class Requester(Thread):
    """Class for running cmc_requests in multithreads and save results of all threads"""
    report_list = []

    def __init__(self, name):
        super(Requester, self).__init__(target=self.job, args=tuple())
        self.name = name
        self.start()

    def job(self):
        self.response = cmc_request(API_KEY)
        Requester.report_list.append(self.response)


def cmc_multirequest() -> list:
    """ Runs cmc_request in several threads.
        Number of threads can be adjusted in settings.py NUMBER_OF_TREADS,
    """
    list_of_threads = []  # defining list for pull of threads
    for thr in range(NUMBER_OF_TREADS):  # building the pull
        list_of_threads.append(Requester(str(thr)))  # appending thread to list
    while list_of_threads:  # Checking if any thread in pull is alive
        for thread in list_of_threads:
            if not thread.is_alive():
                list_of_threads.remove(thread)
    # When all threads are dead returning
    return Requester.report_list


def cmc_multirequest_mock():
    """Returns mock data"""
    return ((355.2207946777344, True, 10047), (347.37515449523926, True, 10047),
            (341.3228988647461, True, 10047), (368.3803081512451, True, 10047),
            (354.0189266204834, True, 10046), (378.342866897583, True, 10047),
            (389.8909091949463, True, 10047), (407.6111316680908, True, 10047))


if __name__ == '__main__':
    if USE_MOCK:
        pprint(cmc_multirequest_mock())
    pprint(cmc_multirequest())
