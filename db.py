import logging

import sqlite3
from sqlite3 import Connection, Cursor

logging.basicConfig(level=logging.INFO)

DB_NAME = 'meetings.db'


class MeetingDbException(Exception):
    pass


class MeetingDb:
    """
    DB wrapper
    """
    conn: Connection
    cur: Cursor

    def __init__(self) -> None:
        global DB_NAME
        self.conn = sqlite3.connect(DB_NAME)

    def __enter__(self):
        self.cur = self.conn.cursor()
        try:
            self.cur.execute("""CREATE TABLE meetings
                            (id INTEGER PRIMARY KEY,
                            description TEXT NOT NULL,
                            start_date TEXT NOT NULL,
                            end_date TEXT NOT NULL)""")
        except sqlite3.OperationalError as e:
            logging.info(f'Cant create meetings table: {str(e)}')

        try:
            self.cur.execute("""CREATE TABLE participants
                            (id INTEGER PRIMARY KEY,
                            meeting_id INTEGER NOT NULL,
                            user_id INTEGER NOT NULL,
                            user_name TEXT NOT NULL)""")
        except sqlite3.OperationalError as e:
            logging.info(f'Cant create participants table: {str(e)}')

        return self

    def __exit__(self, type, value, traceback) -> None:
        self.conn.close()

    def addMeetings(self, descr: str, start_date: str, end_date: str) -> int:
        try:
            self.cur.execute(
                'INSERT INTO meetings(description, start_date, end_date) VALUES (?, ?, ?)',
                (descr, start_date, end_date)
            )
            self.conn.commit()
        except sqlite3.OperationalError as e:
            logging.error(f'Cant add meeting: {str(e)}')
            raise MeetingDbException('Cant add meeting: check logs')

        return self.cur.lastrowid  # type: ignore
