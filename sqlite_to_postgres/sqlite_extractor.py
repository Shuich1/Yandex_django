from classes import Genre, Person, Filmwork, GenreFilmwork, PersonFilmwork


class SQLiteExtractor:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.data = {}

    def extract_all(self):
        self.extract_genres()
        self.extract_persons()
        self.extract_film_works()
        self.extract_genre_film_works()
        self.extract_person_film_works()

        return self.data

    def extract_genres(self):
        self.cursor.execute('SELECT * FROM genre')
        genres = []
        for row in self.cursor.fetchall():
            genre = Genre(
                name=row[1],
                description=row[2],
                created=row[3],
                modified=row[4],
                id=row[0]
            )
            genres.append(genre)
        self.data['genres'] = genres

    def extract_persons(self):
        self.cursor.execute('SELECT * FROM person')
        persons = []
        for row in self.cursor.fetchall():
            person = Person(
                full_name=row[1],
                created=row[2],
                modified=row[3],
                id=row[0]
            )
            persons.append(person)
        self.data['persons'] = persons

    def extract_film_works(self):
        self.cursor.execute('SELECT * FROM film_work')
        filmworks = []
        for row in self.cursor.fetchall():
            filmwork = Filmwork(
                title=row[1],
                description=str(row[2]).replace('\"', '\''),
                creation_date=row[3],
                file_path=row[4],
                type=row[6],
                created=row[7],
                modified=row[8],
                rating=row[5],
                id=row[0]
            )
            filmworks.append(filmwork)
        self.data['film_works'] = filmworks

    def extract_genre_film_works(self):
        self.cursor.execute('SELECT * FROM genre_film_work')
        genre_filmworks = []
        for row in self.cursor.fetchall():
            genre_filmwork = GenreFilmwork(
                created=row[3],
                id=row[0],
                genre_id=row[2],
                film_work_id=row[1]
            )
            genre_filmworks.append(genre_filmwork)
        self.data['genre_film_works'] = genre_filmworks

    def extract_person_film_works(self):
        self.cursor.execute('SELECT * FROM person_film_work')
        person_filmworks = []
        for row in self.cursor.fetchall():
            person_filmwork = PersonFilmwork(
                role=row[3],
                created=row[4],
                id=row[0],
                person_id=row[2],
                film_work_id=row[1]
            )
            person_filmworks.append(person_filmwork)
        self.data['person_film_works'] = person_filmworks
