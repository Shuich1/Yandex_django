from psycopg2.extensions import connection as _connection
import psycopg2
from dotenv import load_dotenv

import os
import logging


class PostgresSaver:
    def __init__(self, connection: _connection):
        self.connection = connection
        self.logger = logging.getLogger(__name__)

    def init_database(self) -> None:
        """Метод для инициализации базы данных"""
        load_dotenv()
        self.logger.info('Initializing database...')
        with self.connection.cursor() as pg_cursor:
            try:
                with open(os.environ.get('DDL_PATH'), 'r') as schema_file:
                    pg_cursor.execute(schema_file.read())
            except Exception:
                self.logger.exception('Error while initializing database')
            self.logger.info('Finished! Database initialized')

    def save_pack(self, table_name: str, pack: list) -> None:
        """Метод для сохранения данных в Postgres"""
        self.logger.info(f'Saving {table_name} pack...')
        with self.connection.cursor() as pg_cursor:
            query = ','.join(
                pg_cursor.mogrify(
                    f'({",".join(["%s"] * len(row))})',
                    row
                ).decode('utf-8') for row in pack
            )
            try:
                pg_cursor.execute(
                    f'INSERT INTO content.{table_name} '
                    f'VALUES {query} ON CONFLICT DO NOTHING'
                )
                self.logger.info(f'Pack {table_name} saved')
            except psycopg2.Error:
                self.logger.exception(
                    f'Not saved {table_name} pack from '
                    f'{pack[0][0]} to {pack[-1][0]}'
                )
            finally:
                self.connection.commit()
