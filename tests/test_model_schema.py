import datetime

import pytest
from peewee import IntegrityError

from songbook import models


def test_tables_exist():
    """Our database has five tables. They are created via `models.init()`."""
    models.init(":memory:")
    assert models._db.table_exists("song")
    assert models._db.table_exists("arrangement")
    assert models._db.table_exists("worship")
    assert models._db.table_exists("worship_song_through")
    assert models._db.table_exists("worship_arrangement_through")


def test_hymn_fields():
    """`Hymn` table has 2 fields, `id` and `name`."""
    hymn = models.Hymn.create(name="Song A", id=1)
    assert hymn.id == 1


def test_hymn_id():
    """The `id` column of `Hymn` does not represent row id's, so they
    do not need to be in sequential order.
    """
    hymn_3 = models.Hymn.create(name="Hymn 3", id=3)
    hymn_2 = models.Hymn.create(name="Hymn 2", id=2)
    assert hymn_2.id == 2
    assert hymn_3.id == 3


def test_song_fields():
    """`Song` table has 3 fields: `name`, `key`, and `hymn_ref`."""
    song = models.Song.create(name="Song A", key="C", hymn=1)
    assert song.hymn.id == 1


def test_song_name_uniqueness():
    """The `name` field in `song` table must be unique."""
    with pytest.raises(IntegrityError):
        models.Song.insert(name="Song A", key="F#m").execute()


def test_song_hymn_ref_nullability():
    """The `hymn_ref` field is nullable."""
    song = models.Song.create(name="Song B", key="Ab")
    assert song.hymn is None


def test_arrangement_field():
    """`arrangement` table has 2 fields: `name` and `role`."""
    arrangement = models.Arrangement.create(name="Adam", role="Lead Singer")
    assert arrangement.name == "Adam"


def test_worship_foreign_keys():
    """`worship` table contains two foreign keys: `song` and `arrangement`."""
    song = models.Song.get(models.Song.name == "Song A")
    another_song = models.Song.get(models.Song.name == "Song B")
    arrangement = models.Arrangement.get(models.Arrangement.name == "Adam")
    another_arrangement = models.Arrangement.create(name="Bella", role="Vocal")

    worship = models.Worship.create(date=datetime.date(2019, 10, 27))
    worship.songs.add([song, another_song])
    worship.arrangements.add([arrangement, another_arrangement])

    worship_songs = [song.name for song in worship.songs.order_by(models.Song.name)]
    worship_arrs = [
        arr.name for arr in worship.arrangements.order_by(models.Arrangement.name)
    ]

    assert worship_songs == ["Song A", "Song B"]
    assert worship_arrs == ["Adam", "Bella"]
