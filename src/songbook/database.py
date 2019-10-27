"""
database.py

This module handles database transactions, and performs CRUD operations.

The Plan:

>>> songbook = SongBook(db_uri='songbook.db')  # db is initialized and connected
>>> songbook.add('song', **kwargs)  # factory method
>>> songbook.view('song', **kwargs)  # also factory, where-clause can be passed as kwargs
>>> # Conveniently,
>>> songbook.songs  # @property, shorthand of songbook.view('song')
>>> songbook.remove('worship', date=date(2019, 10, 12))  # factory
>>> songbook.update('song', **kwargs)
>>> songbook.import(file='songs.csv', table='song', on_conflict='update')

"""

from datetime import date
from typing import Mapping, Sequence, Tuple

from .models import (
    Arrangement,
    Song,
    Worship,
    WorshipArrangement,
    WorshipSong,
    db,
    initialize,
)


def initialize(db_uri: str):
    """Initialize the database with `db_uri`."""
    db.init(db_uri)
    db.create_tables([Song, Arrangement, Worship, WorshipSong, WorshipArrangement])


def add_songs(songs: Sequence[Tuple[str, str, int]]) -> bool:
    """Bulk insert songs into the database."""

    with db.atomic():
        Song.insert_many(songs, fields=[Song.name, Song.key, Song.hymn]).on_conflict(
            conflict_target=[Song.name], preserve=[Song.key, Song.hymn]
        ).execute()


def add_worship(
    date: date, songs: Sequence[str], arrangements: Mapping[str, str]
) -> bool:
    """Add a service into the database."""
    worship = Worship.create(date=date)
    # song_list = Song.select().where(Song.name.in_(songs)).execute()
    arrangement_list = []
    for role, name in arrangements.items():
        arrangement_list.append(Arrangement.get_or_create(role=role, name=name)[0])

    worship.songs.add(Song.select().where(Song.name.in_(songs)))
    worship.arrangements.add(arrangement_list)
