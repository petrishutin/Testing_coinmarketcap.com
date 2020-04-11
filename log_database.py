""" This support module provides database requests function.
    If run alone, returns last commit to log
"""

import sqlite3
from pprint import pprint


def db_req(db: str, req: str) -> 'cursor or None':
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(req)
            respond = cursor.fetchall()
            return respond
        except sqlite3.OperationalError as err:
            print('OperatinalError:', err)
            return


if __name__ == '__main__':
    # shows last commit in log.
    table = db_req('log.db', 'SELECT * FROM log ORDER BY id DESC LIMIT 1;')
    print('Last fixture id:', table[0][0], 'created at:', table[0][1])
    pprint(table[0][2])
