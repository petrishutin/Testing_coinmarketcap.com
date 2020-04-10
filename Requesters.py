from threading import Thread
from cmc_request import cmc_request
from pprint import pprint
from settings import API_KEY, NUMBER_OF_TREADS, USE_MOCK


class Requester(Thread):
    report_list = []

    def __init__(self, name):
        super(Requester, self).__init__(target=self.job, args=tuple())
        self.name = name
        self.start()

    def job(self):
        self.response = cmc_request(API_KEY)
        Requester.report_list.append(self.response)


def cmc_multirequests() -> list:
    list_of_threads = []
    for thr in range(NUMBER_OF_TREADS):
        list_of_threads.append(Requester(str(thr)))
    while list_of_threads:  # checking if
        for thread in list_of_threads:
            if not thread.is_alive():
                list_of_threads.remove(thread)
    return Requester.report_list


def cmc_multirequests_mock():
    return ((200, True, 10000),
            (200, True, 10000),
            (200, True, 10000),
            (200, True, 10000)
            )


if __name__ == '__main__':
    if USE_MOCK:
        pprint(cmc_multirequests_mock())
    pprint(cmc_multirequests())
