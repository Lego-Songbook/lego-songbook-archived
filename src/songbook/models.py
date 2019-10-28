from peewee import (
    CharField,
    DateField,
    ForeignKeyField,
    IntegerField,
    ManyToManyField,
    Model,
    SqliteDatabase,
)

__all__ = ("Song", "Arrangement", "Worship", "Hymn", "init")

_db = SqliteDatabase(None)


class _BaseModel(Model):
    class Meta:
        database = _db

    def __repr__(self):
        data: dict = self.__data__
        fields: list = sorted(list(self._meta.fields.keys()))
        table: str = self._meta.table_name.title()
        field_values = [f"{field}={data.get(field, 'None')}" for field in fields]
        return f"{table}({', '.join(field_values)})"

    __str__ = __repr__


class Hymn(_BaseModel):

    index = IntegerField(primary_key=True)
    name = CharField()
    key = CharField()


class Song(_BaseModel):

    name = CharField(unique=True)
    key = CharField(null=True)
    hymn = ForeignKeyField(Hymn, null=True)


class Arrangement(_BaseModel):

    name = CharField()
    role = CharField()


class Worship(_BaseModel):

    date = DateField()
    songs = ManyToManyField(Song)
    arrangements = ManyToManyField(Arrangement)


WorshipSong = Worship.songs.get_through_model()
WorshipArrangement = Worship.arrangements.get_through_model()


def init(db_uri: str):
    """Initialize the database with `db_uri`."""
    _db.init(db_uri)  # TODO: Add path validation.
    _db.create_tables(
        [Hymn, Song, Arrangement, Worship, WorshipSong, WorshipArrangement]
    )
