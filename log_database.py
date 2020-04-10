import sqlite3


def db_req(db: str, req: str) -> 'cursor or None':
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(req)
            respond = cursor.fetchall()
            return respond
        except sqlite3.OperationalError as err:
            print('OperatinalError:', err, 'An input must be a valid sql request')
            return []

