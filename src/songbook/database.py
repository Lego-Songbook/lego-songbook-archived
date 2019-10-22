from datetime import date
from typing import Mapping, Sequence, Tuple

from .models import Arrangement, Song, Worship, db, WorshipSong, WorshipArrangement


def initialize(db_uri: str):
    """Initialize the database with `db_uri`."""
    db.init(db_uri)
    db.create_tables([Song, Arrangement, Worship, WorshipSong, WorshipArrangement])


def add_songs(songs: Sequence[Tuple[str, str, int]]) -> bool:
    """Bulk insert songs into the database."""

    with db.atomic():
        Song.insert_many(
            songs, fields=[Song.name, Song.key, Song.hymn_ref]
        ).on_conflict(
            conflict_target=[Song.name], preserve=[Song.key, Song.hymn_ref]
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


def import_songs_by_sheet_names():
    """Bulk import songs by sheet names."""
