from threading import Thread
from cmc_request import cmc_request
from pprint import pprint


class Requester(Thread):
    with open('API_KEY.txt', 'r') as file:
        API_KEY = file.readline()
    report_list = []

    def __init__(self, name):
        super(Requester, self).__init__(target=self.job, args=tuple())
        self.name = name
        self.start()

    def job(self):
        self.response = cmc_request(Requester.API_KEY)
        Requester.report_list.append(self.response)


def cmc_multirequests(number_of_threads: int = 8):
    list_of_threads = []
    for thr in range(number_of_threads):
        list_of_threads.append(Requester(str(thr)))
    while list_of_threads:  # checking if
        for thread in list_of_threads:
            if not thread.is_alive():
                list_of_threads.remove(thread)
    return Requester.report_list


if __name__ == '__main__':
    pprint(cmc_multirequests())
