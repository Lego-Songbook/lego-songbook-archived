import datetime

import pytest
from peewee import IntegrityError

from songbook import models
from songbook.models import *


def test_tables_exist():
    """Our database has five tables. They are created via `models.init()`."""
    models.init(":memory:")
    tables = [
        "artist",
        "arrangement",
        "hymn",
        "key",
        "person",
        "role",
        "song",
        "worship",
        "worship_song",
        "worship_arrangement",
    ]
    for table in tables:
        assert models._db.table_exists(table)


def test_key():
    """`Key` has 2 fields, `id` and `name`."""
    key = Key.create(name="C", id=1)
    assert key.name == "C"
    assert key.id == 1


def test_key_uniqueness():
    """`Key.name` is a unique field."""
    with pytest.raises(IntegrityError):
        Key.create(id=2, name="C")


def test_artist():
    """`Artist` has 2 fields, `id` and `name`."""
    sop = Artist.create(id=1, name="Stream of Praise")
    assert sop.name == "Stream of Praise"
    assert sop.id == 1


def test_hymn_fields():
    """`Hymn` table has 3 fields, `id`, `name`, and `key`."""
    hymn = models.Hymn.create(name="Hymn 1", id=1, key=1)
    assert hymn.id == 1
    assert hymn.name == "Hymn 1"
    assert hymn.key_id == 1


def test_hymn_key_is_null():
    """`Hymn.key` is nullable."""
    hymn = Hymn.create(name="Hymn 2", id=2)
    assert hymn.key is None


def test_hymn_id_order():
    """The `id` column of `Hymn` does not represent row id's, so they
    do not need to be in sequential order.
    """
    hymn_4 = Hymn.create(name="Hymn 4", id=4)
    hymn_3 = Hymn.create(name="Hymn 3", id=3)
    assert hymn_3.id == 3
    assert hymn_4.id == 4


def test_song_fields():
    """`Song` table has many fields."""
    song = Song.create(
        id=1, name="Song A", key=1, hymn=1, artist=1, tempo=120, scripture="Psalm 27:4"
    )
    assert song.id == 1
    assert song.name == "Song A"
    assert song.hymn_id == 1
    assert song.artist_id == 1
    assert song.tempo == 120
    assert song.scripture == "Psalm 27:4"


def test_song_nullable_fields():
    """The key, hymn, artist, tempo, and scripture fields are nullable in `Song`."""
    song = Song.create(id=2, name="Song B")
    assert song.id == 2
    assert song.name == "Song B"
    assert song.hymn_id is None
    assert song.artist_id is None
    assert song.tempo is None
    assert song.scripture is None


def test_song_name_uniqueness():
    """`Song.name` need not to be unique."""
    song = Song.create(id=3, name="Song B")
    q = song.select().where(Song.name == "Song B").order_by(Song.id.asc()).execute()
    assert list(map(lambda x: x.id, q)) == [2, 3]


def test_person_fields():
    """`Person` has 2 fields."""
    person = Person.create(id=1, name="Adam")
    assert person.id == 1
    assert person.name == "Adam"


def test_person_name_uniqueness():
    """`Person.name` is unique."""
    with pytest.raises(IntegrityError):
        Person.create(id=2, name="Adam")


def test_role_fields():
    """`Role` has 2 fields."""
    role = Role.create(id=1, name="leader")
    assert role.id == 1
    assert role.name == "leader"


def test_role_name_uniqueness():
    """`Role.name` is unique."""
    with pytest.raises(IntegrityError):
        Role.create(id=2, name="leader")


def test_arrangement_field():
    """`Arrangement` table has 2 fields: `name` and `role`."""
    arrangement = Arrangement.create(person=1, role=1)
    assert arrangement.person.name == "Adam"
    assert arrangement.role.name == "leader"


def test_worship_field():
    """`Worship` has 2 fields, `id` and `date`."""
    worship = Worship.create(id=1, date=datetime.date(2019, 10, 27))
    assert worship.id == 1
    assert worship.date == datetime.date(2019, 10, 27)


def test_worship_song_fields():
    """`WorshipSong` holds info about songs in a worship."""
    WorshipSong.insert_many(
        [(1, 1, 1), (2, 1, 2), (3, 1, 3)],
        fields=[WorshipSong.id, WorshipSong.worship, WorshipSong.song],
    ).execute()
    q = (
        Song.select()
        .join(WorshipSong)
        .join(Worship)
        .where(Worship.date == datetime.date(2019, 10, 27))
    )
    assert [e.id for e in q] == [1, 2, 3]


def test_worship_arrangement_fields():
    """`WorshipArrangement` holds info about arrangements in a worship."""
    WorshipArrangement.insert_many(
        [(1, 1, 1)],
        fields=[
            WorshipArrangement.id,
            WorshipArrangement.worship,
            WorshipArrangement.arrangement,
        ],
    ).execute()
    q = (
        Arrangement.select(Arrangement, Person, Role)
        .join(Person)
        .switch(Arrangement)
        .join(Role)
        .switch(Arrangement)
        .join(WorshipArrangement)
        .join(Worship)
        .where(Worship.date == datetime.date(2019, 10, 27))
    )
    assert [f"{e.role.name}: {e.person.name}" for e in q] == ["leader: Adam"]
