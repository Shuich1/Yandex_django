import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from dotenv import load_dotenv
import os

from sqlite_extractor import SQLiteExtractor
from postgres_saver import PostgresSaver


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    sqlite_extractor = SQLiteExtractor(connection)
    data = sqlite_extractor.extract_all()
    postgres_saver = PostgresSaver(pg_conn, data)
    postgres_saver.save_all()


if __name__ == '__main__':
    load_dotenv()
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT')
    }
    with sqlite3.connect(
        os.environ.get('DB_SQLITE_PATH')) as sqlite_conn,\
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
