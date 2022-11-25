import uuid
from dataclasses import dataclass, field


@dataclass
class Genre:
    name: str
    description: str
    created: str
    modified: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person:
    full_name: str
    created: str
    modified: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Filmwork:
    title: str
    description: str
    creation_date: str
    file_path: str
    type: str
    created: str
    modified: str
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class GenreFilmwork:
    created: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonFilmwork:
    role: str
    created: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
