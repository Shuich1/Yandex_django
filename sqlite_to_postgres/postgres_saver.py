from psycopg2.extensions import connection as _connection
from tqdm import tqdm
import time


class PostgresSaver:
    def __init__(self, connection: _connection, data: dict):
        self.connection = connection
        self.cursor = connection.cursor()

        self.data = data

    def save_all(self):
        """Метод для сохранения всех данных в базу данных Postgres"""
        self.save_genres()
        self.save_persons(pack_size=400)
        self.save_film_works(pack_size=500)
        self.save_genre_film_works(pack_size=500)
        self.save_person_film_works(pack_size=1000)
        self.connection.commit()

    def pack_saver(self, pack_size, counter):
        """Метод для сохранения пакетов данных в базу данных Postgres"""
        counter += 1
        if counter < pack_size:
            return counter
        self.connection.commit()
        time.sleep(0.5)
        return 0

    def save_genres(self, pack_size=100):
        """Метод для сохранения жанров в базу данных Postgres"""
        counter = 0
        for genre in tqdm(self.data['genres']):
            query = self.cursor.mogrify("""
                INSERT INTO content.genre
                (id, name, description, created, modified)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """, (
                    genre.id,
                    genre.name,
                    genre.description,
                    genre.created,
                    genre.modified
                )
            )
            self.cursor.execute(query)
            counter = self.pack_saver(pack_size, counter)

    def save_persons(self, pack_size=100):
        """Метод для сохранения персон в базу данных Postgres"""
        counter = 0
        for person in tqdm(self.data['persons']):
            query = self.cursor.mogrify("""
                INSERT INTO content.person
                (id, full_name, created, modified)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """, (
                    person.id,
                    person.full_name,
                    person.created,
                    person.modified
                    )
                )
            self.cursor.execute(query)
            counter = self.pack_saver(pack_size, counter)

    def save_film_works(self, pack_size=100):
        """Метод для сохранения фильмов в базу данных Postgres"""
        counter = 0
        for film_work in tqdm(self.data['film_works']):
            query = self.cursor.mogrify("""
                INSERT INTO content.film_work
                (id, title, description, creation_date,
                rating, type, created, modified, file_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """, (
                    film_work.id,
                    film_work.title,
                    film_work.description,
                    film_work.creation_date,
                    film_work.rating,
                    film_work.type,
                    film_work.created,
                    film_work.modified,
                    film_work.file_path
                    )
            )
            self.cursor.execute(query)
            counter = self.pack_saver(pack_size, counter)

    def save_genre_film_works(self, pack_size=100):
        """Метод для сохранения жанров фильмов в базу данных Postgres"""
        counter = 0
        for genre_film_work in tqdm(self.data['genre_film_works']):
            query = self.cursor.mogrify("""
                INSERT INTO content.genre_film_work
                (id, genre_id, film_work_id, created)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """, (
                    genre_film_work.id,
                    genre_film_work.genre_id,
                    genre_film_work.film_work_id,
                    genre_film_work.created
                    )
            )
            self.cursor.execute(query)
            self.connection.commit()
            counter = self.pack_saver(pack_size, counter)

    def save_person_film_works(self, pack_size=100):
        """Метод для сохранения персон фильмов в базу данных Postgres"""
        counter = 0
        for person_film_work in tqdm(self.data['person_film_works']):
            query = self.cursor.mogrify("""
                INSERT INTO content.person_film_work
                (id, person_id, film_work_id, role, created)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """, (
                    person_film_work.id,
                    person_film_work.person_id,
                    person_film_work.film_work_id,
                    person_film_work.role,
                    person_film_work.created
                    )
            )
            self.cursor.execute(query)
            counter = self.pack_saver(pack_size, counter)
