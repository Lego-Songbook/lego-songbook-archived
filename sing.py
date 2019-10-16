from datetime import date
from typing import Sequence, Tuple, Mapping

from peewee import (
    CharField,
    DateField,
    IntegerField,
    ManyToManyField,
    SqliteDatabase,
    Model,
)

db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class Song(BaseModel):

    name = CharField(unique=True)
    key = CharField()
    hymn_ref = IntegerField(null=True)

    def __repr__(self):
        return f"Song(id={self.id}, name={self.name}, key={self.key}, hymn_ref={self.hymn_ref})"


class Arrangement(BaseModel):

    name = CharField()
    role = CharField()

    def __repr__(self):
        return f"Arrangement(id={self.id}, role={self.role}, name={self.name})"


class Worship(BaseModel):

    date = DateField()
    songs = ManyToManyField(Song)
    arrangements = ManyToManyField(Arrangement)

    def __repr__(self):
        return f"Worship(id={self.id}, date={self.date}, songs={[song for song in self.songs]}, arrangements={[arr for arr in self.arrangements]})"


WorshipSong = Worship.songs.get_through_model()
WorshipArrangement = Worship.arrangements.get_through_model()


def initialize(db_uri):
    db.init(db_uri)
    db.create_tables([Song, Arrangement, Worship, WorshipSong, WorshipArrangement])


# def add_song(name: str, key: str, hymn_ref: int = None) -> bool:
#     """Add a song into the database.
#
#     :param name: the name of the song
#     :param key: the key of the song
#     :param hymn_ref: the index number of the song in Hymn
#
#     Example:
#     >>> add_song(name="Song A", key="Bb", hymn_ref=253)
#     True
#
#     """
#     Song.create(name=name, key=key, hymn_ref=hymn_ref)


def add_songs(songs: Sequence[Tuple[str, str, int]]) -> bool:
    """Bulk insert songs into the database."""

    with db.atomic():
        Song.insert_many(songs, fields=[Song.name, Song.key, Song.hymn_ref]
            ).on_conflict(
                conflict_target=[Song.name],
                preserve=[Song.key, Song.hymn_ref],
            ).execute()
# 
#
# def add_arrangements(arrangements: Mapping[str, str]) -> bool:
#     """Add an arrangement into the database.
#
#     :param arrangements: a dictionary of role: name pairs
#
#     Example:
#     >>> add_arrangement({"Leader": "Adam", "Keyboard": "Bella"})
#     True
#
#     """
#     # arrangement_data = [(role, name) for role, name in arrangements.items()]
#     with db.atomic():
#         Arrangement.insert_many(
#             arrangements.items(), fields=[Arrangement.role, Arrangement.name]
#         ).on_conflict_ignore().execute()


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
