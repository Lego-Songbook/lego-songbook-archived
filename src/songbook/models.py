from typing import Any, Dict, List, Tuple, Union

from peewee import (
    CharField,
    DateField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
)

db = SqliteDatabase(None)


class _BaseModel(Model):
    class Meta:
        database = db
        legacy_table_names = False

    def __repr__(self):
        data: Dict[str, Any] = self.__data__
        fields: List[str] = list(self._meta.fields.keys())
        table: str = self._meta.table_name.title()
        field_values: List[str] = [
            f"{field}={data.get(field, 'None')}" for field in fields
        ]
        return f"{table}({', '.join(field_values)})"

    @classmethod
    def table_name(cls) -> str:
        return cls._meta.table_name

    @classmethod
    def fields(cls) -> List[str]:
        if cls._meta.fields is None:
            return []
        return list(cls._meta.fields.keys())


class Key(_BaseModel):
    """The key of a song, such as F# or Abm."""

    id = IntegerField(primary_key=True)
    name = CharField(unique=True)


class Artist(_BaseModel):
    """The artist of a song."""

    id = IntegerField(primary_key=True)
    name = CharField()


class Hymn(_BaseModel):
    """The official Hymn Book the church uses."""

    id = IntegerField(primary_key=True)
    name = CharField()
    key = ForeignKeyField(Key, null=True)


class Song(_BaseModel):
    """A piece of song."""

    id = IntegerField(primary_key=True)
    name = CharField()
    key = ForeignKeyField(Key, null=True)
    hymn = ForeignKeyField(Hymn, null=True)
    artist = ForeignKeyField(Artist, null=True)
    tempo = IntegerField(null=True)
    scripture = CharField(null=True)


class Person(_BaseModel):
    """A person who plays an instrument or have a role in a worship."""

    id = IntegerField(primary_key=True)
    name = CharField(unique=True)


class Role(_BaseModel):
    """A role a person takes in a worship, can be an instrument or vocal roles."""

    id = IntegerField(primary_key=True)
    name = CharField(unique=True)


class Arrangement(_BaseModel):
    """A possible combination of `Person` and `Role`."""

    id = IntegerField(primary_key=True)
    person = ForeignKeyField(Person)
    role = ForeignKeyField(Role)


class Worship(_BaseModel):
    """A worship event."""

    id = IntegerField(primary_key=True)
    date = DateField()


class WorshipSong(_BaseModel):
    """The songs in a worship."""

    id = IntegerField(primary_key=True)
    worship = ForeignKeyField(Worship)
    song = ForeignKeyField(Song)


class WorshipArrangement(_BaseModel):
    """The instrumentation & vocal arrangements in a worship."""

    id = IntegerField(primary_key=True)
    worship = ForeignKeyField(Worship)
    arrangement = ForeignKeyField(Arrangement)


TABLES = [
    Arrangement,
    Artist,
    Hymn,
    Key,
    Person,
    Role,
    Song,
    Worship,
    WorshipArrangement,
    WorshipSong,
]


def init(db_uri: str):
    """Initialize the database with `db_uri`."""
    db.init(db_uri)  # TODO: Add path validation.
    db.create_tables(TABLES)
