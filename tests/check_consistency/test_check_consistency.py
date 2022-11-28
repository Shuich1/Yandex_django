import sqlite3
import psycopg2

import pytest

import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
dsl = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT')
}


@pytest.fixture
def db_connect():
    """Фикстура для подключения к БД"""
    with sqlite3.connect(
        os.environ.get('DB_SQLITE_PATH')) as sqlite_conn,\
            psycopg2.connect(**dsl) as pg_conn:
        yield sqlite_conn, pg_conn


def test_amount_genre(db_connect):
    """Тест для проверки соответствия количества жанров"""
    sqlite_cursor, psycopg2_cursor = db_connect[0].cursor(), db_connect[1].cursor()
    sqlite_cursor.execute('SELECT COUNT(*) FROM genre')
    psycopg2_cursor.execute('SELECT COUNT(*) FROM content.genre')
    assert sqlite_cursor.fetchone()[0] == psycopg2_cursor.fetchone()[0]


def test_amount_person(db_connect):
    """Тест для проверки соответствия количества персон"""
    sqlite_cursor, psycopg2_cursor = db_connect[0].cursor(), db_connect[1].cursor()
    sqlite_cursor.execute('SELECT COUNT(*) FROM person')
    psycopg2_cursor.execute('SELECT COUNT(*) FROM content.person')
    assert sqlite_cursor.fetchone()[0] == psycopg2_cursor.fetchone()[0]


def test_amount_film_work(db_connect):
    """Тест для проверки соответствия количества фильмов"""
    sqlite_cursor, psycopg2_cursor = db_connect[0].cursor(), db_connect[1].cursor()
    sqlite_cursor.execute('SELECT COUNT(*) FROM film_work')
    psycopg2_cursor.execute('SELECT COUNT(*) FROM content.film_work')
    assert sqlite_cursor.fetchone()[0] == psycopg2_cursor.fetchone()[0]


def test_amount_genre_film_work(db_connect):
    """Тест для проверки соответствия количества жанров фильмов"""
    sqlite_cursor, psycopg2_cursor = db_connect[0].cursor(), db_connect[1].cursor()
    sqlite_cursor.execute('SELECT COUNT(*) FROM genre_film_work')
    psycopg2_cursor.execute('SELECT COUNT(*) FROM content.genre_film_work')
    assert sqlite_cursor.fetchone()[0] == psycopg2_cursor.fetchone()[0]


def test_amount_person_film_work(db_connect):
    """Тест для проверки соответствия количества персон фильмов"""
    sqlite_cursor, psycopg2_cursor = db_connect[0].cursor(), db_connect[1].cursor()
    sqlite_cursor.execute('SELECT COUNT(*) FROM person_film_work')
    psycopg2_cursor.execute('SELECT COUNT(*) FROM content.person_film_work')
    assert sqlite_cursor.fetchone()[0] == psycopg2_cursor.fetchone()[0]


def extract_pack(cursor, table_name):
    """Функция для извлечения данных из таблицы"""
    cursor.execute(f'SELECT * FROM {table_name}')
    while True:
        pack = cursor.fetchmany(100)
        if pack:
            yield pack
        else:
            break

def test_content_genre(db_connect):
    """Тест для проверки соответствия жанров"""
    sqlite_cursor, psycopg2_cursor = db_connect[0].cursor(), db_connect[1].cursor()
    sqlite_cursor.execute('SELECT * FROM genre')
    psycopg2_cursor.execute('SELECT * FROM content.genre')

    for sqlite_pack, pg_pack in zip(extract_pack(sqlite_cursor, 'genre'), extract_pack(psycopg2_cursor, 'content.genre')):
        for sqlite_row, pg_row in zip(sqlite_pack, pg_pack):
            assert sqlite_row[0] == pg_row[0]
            assert sqlite_row[1] == pg_row[1]
            assert sqlite_row[2] == pg_row[2]
            assert datetime.strptime(sqlite_row[3]+"00", "%Y-%m-%d %H:%M:%S.%f%z") == pg_row[3]
            assert datetime.strptime(sqlite_row[4]+"00", "%Y-%m-%d %H:%M:%S.%f%z") == pg_row[4]


def test_content_person(db_connect):
    """Тест для проверки соответствия персон"""
    sqlite_cursor, psycopg2_cursor = db_connect[0].cursor(), db_connect[1].cursor()
    sqlite_cursor.execute('SELECT * FROM person')
    psycopg2_cursor.execute('SELECT * FROM content.person')

    for sqlite_pack, pg_pack in zip(extract_pack(sqlite_cursor, 'person'), extract_pack(psycopg2_cursor, 'content.person')):
        for sqlite_row, pg_row in zip(sqlite_pack, pg_pack):
            assert sqlite_row[0] == pg_row[0]
            assert sqlite_row[1] == pg_row[1]
            assert datetime.strptime(sqlite_row[2]+"00", "%Y-%m-%d %H:%M:%S.%f%z") == pg_row[2]
            assert datetime.strptime(sqlite_row[3]+"00", "%Y-%m-%d %H:%M:%S.%f%z") == pg_row[3]


def test_content_film_work(db_connect):
    """Тест для проверки соответствия фильмов"""
    sqlite_cursor, psycopg2_cursor = db_connect[0].cursor(), db_connect[1].cursor()
    sqlite_cursor.execute('SELECT * FROM film_work')
    psycopg2_cursor.execute('SELECT * FROM content.film_work')

    for sqlite_pack, pg_pack in zip(extract_pack(sqlite_cursor, 'film_work'), extract_pack(psycopg2_cursor, 'content.film_work')):
        for sqlite_row, pg_row in zip(sqlite_pack, pg_pack):
            sqlite_row, pg_row = list(sqlite_row), list(pg_row)
            assert sqlite_row[0] == pg_row[0]
            assert sqlite_row[1] == pg_row[1]
            assert sqlite_row[2] == pg_row[2]
            if sqlite_row[3] is None:
                assert pg_row[3] is None
            else:
                assert datetime.strptime(sqlite_row[3]+"00", "%Y-%m-%d %H:%M:%S.%f%z") == pg_row[3]
            assert sqlite_row[4] == pg_row[4]
            assert sqlite_row[5] == pg_row[5]
            assert sqlite_row[6] == pg_row[6]
            assert datetime.strptime(sqlite_row[7]+"00", "%Y-%m-%d %H:%M:%S.%f%z") == pg_row[7]
            assert datetime.strptime(sqlite_row[8]+"00", "%Y-%m-%d %H:%M:%S.%f%z") == pg_row[8]


def test_content_genre_film_work(db_connect):
    """Тест для проверки соответствия жанров фильмов"""
    sqlite_cursor, psycopg2_cursor = db_connect[0].cursor(), db_connect[1].cursor()
    sqlite_cursor.execute('SELECT * FROM genre_film_work')
    psycopg2_cursor.execute('SELECT * FROM content.genre_film_work')

    for sqlite_pack, pg_pack in zip(extract_pack(sqlite_cursor, 'genre_film_work'), extract_pack(psycopg2_cursor, 'content.genre_film_work')):
        for sqlite_row, pg_row in zip(sqlite_pack, pg_pack):
            assert sqlite_row[0] == pg_row[0]
            assert sqlite_row[1] == pg_row[1]
            assert sqlite_row[2] == pg_row[2]
            assert datetime.strptime(sqlite_row[3]+"00", "%Y-%m-%d %H:%M:%S.%f%z") == pg_row[3]


def test_content_person_film_work(db_connect):
    """Тест для проверки соответствия персон фильмов"""
    sqlite_cursor, psycopg2_cursor = db_connect[0].cursor(), db_connect[1].cursor()
    sqlite_cursor.execute('SELECT * FROM person_film_work')
    psycopg2_cursor.execute('SELECT * FROM content.person_film_work')

    for sqlite_pack, pg_pack in zip(extract_pack(sqlite_cursor, 'person_film_work'), extract_pack(psycopg2_cursor, 'content.person_film_work')):

        for sqlite_row, pg_row in zip(sqlite_pack, pg_pack):
            assert sqlite_row[0] == pg_row[0]
            assert sqlite_row[1] == pg_row[1]
            assert sqlite_row[2] == pg_row[2]
            assert sqlite_row[3] == pg_row[3]
            assert datetime.strptime(sqlite_row[4]+"00", "%Y-%m-%d %H:%M:%S.%f%z") == pg_row[4]
