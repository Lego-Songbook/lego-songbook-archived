from datetime import date
from typing import Sequence, Tuple

from peewee import *


db = SqliteDatabase("songbook.db")


class BaseModel(Model):
    class Meta:
        database = db


class Song(BaseModel):

    name = CharField()
    key = CharField()
    hymn_ref = IntegerField()


class Arrangement(BaseModel):

    name = CharField()
    role = CharField()


class Worship(BaseModel):

    date = DateField()
    songs = ManyToManyField(Song)
    arrangements = ManyToManyField(Arrangement)


# worship = Worship.create(date=date(2019, 10, 6))
# song1 = Song.get(Song.name == 'song1')
# song2 = Song.get(Song.name == 'song2')
# arr1 = Arrangement.get(Arrangement.role='keyboard', Arrangement.name='Adam')
# worship.songs.add([song1, song2])
# worship.arrangements.add([arr1])


WorshipSong = Worship.songs.get_through_model()
WorshipArrangement = Worship.arrangements.get_through_model()


# class WorshipSong(BaseModel):
#     worship = ForeignKeyField(Worship)
#     song = ForeignKeyField(Song)
#
#
# class WorshipArrangement(BaseModel):
#
#     worship = ForeignKeyField(Worship)
#     arrangement = ForeignKeyField(Arrangement)


db.create_tables([Song, Arrangement, Worship, WorshipSong, WorshipArrangement])


def add_song(name: str, key: str, hymn_ref: int = 0) -> bool:
    """Add a song into the database.

    :param name: the name of the song
    :param key: the key of the song
    :param hymn_ref: the index number of the song in Hymn

    Example:
    >>> add_song(name="Song A", key="Bb", hymn_ref=253)
    True

    """
    Song.create(name=name, key=key, hymn_ref=hymn_ref)


def add_songs(songs: Sequence[Tuple]) -> bool:
    """Bulk insert songs into the database."""

    with db.atomic():
        Song.insert_many(songs, fields=[Song.name, Song.key, Song.hymn_ref]).execute()


def add_arrangement(date: date, **arrangements) -> bool:
    """Add an arrangement into the database.

    :param date: the service's date
    :param arrangement: a list of arrangement tuple

    Example:
    >>> add_arrangement(
    ...     date='2019-10-06',
    ...     arrangement=[('lead', 'Adam'), ('keyboard', 'Bella')],
    ... )
    True

    """
    arrangement_data = [(date, role, name) for role, name in arrangements]
    with db.atomic():
        Arrangement.insert_many(
            arrangement_data,
            fields=[Arrangement.date, Arrangement.role, Arrangement.name]
        ).execute()


def add_worship(date: date, songs: Sequence[str], **arrangements) -> bool:
    """Add a service into the database."""
    worship = Worship.create(date=date)
    arrangement_data = [(date, role, name, worship) for role, name in arrangements]
    with db.atomic():
        Arrangement.insert_many(
            arrangement_data,
            fields=[Arrangement.date, Arrangement.role, Arrangement.name, Arrangement.worship]
        ).execute()
