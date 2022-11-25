import io


class PostgresSaver:
    def __init__(self, connection, data):
        self.connection = connection
        self.data = data
        self.cursor = connection.cursor()

    def save_all(self):
        self.save_genres()
        self.save_persons()
        self.save_film_works()
        self.save_genre_film_works()
        self.save_person_film_works()
        self.connection.commit()

    def save_genres(self):
        data_for_copy = io.StringIO()
        for genre in self.data['genres']:
            data_for_copy.write(
                f'{genre.id},'
                f'{genre.name},'
                f'{genre.description},'
                f'{genre.created},'
                f'{genre.modified}\n'
            )

        data_for_copy.seek(0)

        self.cursor.copy_expert(
            "COPY content.genre FROM stdin csv NULL 'None'",
            data_for_copy
        )
        self.cursor.execute("select count(*) from content.genre")

    def save_persons(self):
        data_for_copy = io.StringIO()
        for person in self.data['persons']:
            data_for_copy.write(
                f'{person.id},'
                f'{person.full_name},'
                f'{person.created},'
                f'{person.modified}\n'
            )

        data_for_copy.seek(0)

        self.cursor.copy_expert(
            "COPY content.person FROM stdin csv NULL 'None'",
            data_for_copy
        )
        self.cursor.execute("select count(*) from content.person")

    def save_film_works(self):
        data_for_copy = io.StringIO()
        for film_work in self.data['film_works']:
            data_for_copy.write(
                f'{film_work.id}|'
                f'{film_work.title}|'
                f'{film_work.description}|'
                f'{film_work.creation_date}|'
                f'{film_work.rating}|'
                f'{film_work.type}|'
                f'{film_work.created}|'
                f'{film_work.modified}|'
                f'{film_work.file_path}\n'
            )

        data_for_copy.seek(0)
        self.cursor.copy_expert(
            "COPY content.film_work FROM stdin csv delimiter '|' NULL 'None'",
            data_for_copy
        )

    def save_genre_film_works(self):
        data_for_copy = io.StringIO()
        for genre_film_work in self.data['genre_film_works']:
            data_for_copy.write(
                f'{genre_film_work.id},'
                f'{genre_film_work.genre_id},'
                f'{genre_film_work.film_work_id},'
                f'{genre_film_work.created}\n'
            )

        data_for_copy.seek(0)
        self.cursor.copy_expert(
            "COPY content.genre_film_work FROM stdin csv NULL 'None'",
            data_for_copy
        )

    def save_person_film_works(self):
        data_for_copy = io.StringIO()
        for person_film_work in self.data['person_film_works']:
            data_for_copy.write(
                f'{person_film_work.id},'
                f'{person_film_work.person_id},'
                f'{person_film_work.film_work_id},'
                f'{person_film_work.role},'
                f'{person_film_work.created}\n'
            )

        data_for_copy.seek(0)
        self.cursor.copy_expert(
            "COPY content.person_film_work FROM stdin csv NULL 'None'",
            data_for_copy
        )
