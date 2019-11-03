import datetime

import pytest
from peewee import IntegrityError

# from songbook.models import *
from songbook.models import (
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
)

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


@pytest.mark.parametrize("table", tables)
def test_tables_exist(table, test_db):
    """Our database has 10 tables. They are created via `models.init()`."""
    assert test_db.table_exists(table)


@pytest.mark.usefixtures("test_db")
@pytest.mark.parametrize("row", range(1, 4))
def test_key(row):
    """`Key` has 2 fields, `id` and `name`."""
    key = Key.get_by_id(row)
    assert key.name == f"Key {row}"


@pytest.mark.usefixtures("test_db")
def test_key_uniqueness():
    """`Key.name` is a unique field."""
    with pytest.raises(IntegrityError):
        Key.create(id=4, name="Key 1")


@pytest.mark.usefixtures("test_db")
@pytest.mark.parametrize("row", range(1, 4))
def test_artist(row):
    """`Artist` has 2 fields, `id` and `name`."""
    sop = Artist.get_by_id(row)
    assert sop.name == f"Artist {row}"
    assert sop.id == row


@pytest.mark.usefixtures("test_db")
@pytest.mark.parametrize("row", range(1, 4))
def test_hymn_fields(row):
    """`Hymn` table has 3 fields, `id`, `name`, and `key`."""
    hymn = Hymn.get_by_id(row)
    assert hymn.id == row
    assert hymn.name == f"Hymn {row}"
    assert hymn.key_id == row


@pytest.mark.usefixtures("test_db")
def test_hymn_key_is_null():
    """`Hymn.key` is nullable."""
    hymn = Hymn.create(name="Hymn 4", id=4)
    assert hymn.key is None


@pytest.mark.usefixtures("test_db")
def test_hymn_id_order():
    """The `id` column of `Hymn` does not represent row id's, so they
    do not need to be in sequential order.
    """
    hymn_5 = Hymn.create(name="Hymn 5", id=5)
    hymn_4 = Hymn.create(name="Hymn 4", id=4)
    assert hymn_4.id == 4
    assert hymn_5.id == 5


@pytest.mark.usefixtures("test_db")
@pytest.mark.parametrize("row", range(1, 4))
def test_song_fields(row):
    """`Song` table has many fields."""
    song = Song.get_by_id(row)
    assert song.id == row
    assert song.name == f"Song {row}"
    assert song.hymn_id == row
    assert song.artist_id == row
    assert song.tempo == row * 100
    assert song.scripture == f"Scripture {row}"


@pytest.mark.usefixtures("test_db")
def test_song_nullable_fields():
    """The key, hymn, artist, tempo, and scripture fields are nullable in `Song`."""
    song = Song.create(id=4, name="Song 4")
    assert song.hymn_id is None
    assert song.artist_id is None
    assert song.tempo is None
    assert song.scripture is None


@pytest.mark.usefixtures("test_db")
def test_song_name_uniqueness():
    """`Song.name` need not to be unique."""
    Song.create(id=4, name="Song B")
    Song.create(id=5, name="Song B")
    q = Song.select().where(Song.name == "Song B").order_by(Song.id.asc()).execute()
    assert list(map(lambda x: x.id, q)) == [4, 5]


@pytest.mark.usefixtures("test_db")
@pytest.mark.parametrize("row", range(1, 4))
def test_person_fields(row):
    """`Person` has 2 fields."""
    person = Person.get_by_id(row)
    assert person.id == row
    assert person.name == f"Person {row}"


@pytest.mark.usefixtures("test_db")
def test_person_name_uniqueness():
    """`Person.name` is unique."""
    with pytest.raises(IntegrityError):
        Person.create(id=4, name="Person 1")


@pytest.mark.usefixtures("test_db")
@pytest.mark.parametrize("row", range(1, 4))
def test_role_fields(row):
    """`Role` has 2 fields."""
    role = Role.get_by_id(row)
    assert role.id == row
    assert role.name == f"Role {row}"


@pytest.mark.usefixtures("test_db")
def test_role_name_uniqueness():
    """`Role.name` is unique."""
    with pytest.raises(IntegrityError):
        Role.create(id=4, name="Role 1")


@pytest.mark.usefixtures("test_db")
@pytest.mark.parametrize("row", range(1, 4))
def test_arrangement_field(row):
    """`Arrangement` table has 2 fields: `name` and `role`."""
    arrangement = (
        Arrangement.select(Arrangement, Person, Role)
        .join_from(Arrangement, Person)
        .join_from(Arrangement, Role)
        .where(Arrangement.id == row)
        .get()
    )
    assert arrangement.person.name == f"Person {row}"
    assert arrangement.role.name == f"Role {row}"


@pytest.mark.usefixtures("test_db")
@pytest.mark.parametrize("row", range(1, 4))
def test_worship_field(row):
    """`Worship` has 2 fields, `id` and `date`."""
    worship = Worship.get_by_id(row)
    assert worship.id == row
    assert worship.date == datetime.date(2019, row, 1)


def test_worship_song_fields(test_db):
    """`WorshipSong` holds info about songs in a worship."""
    q = (
        Song.select()
        .join(WorshipSong)
        .join(Worship)
        .where(Worship.date == datetime.date(2019, 1, 1))
    )
    assert [e.id for e in q] == [1, 2, 3]


def test_worship_arrangement_fields(test_db):
    """`WorshipArrangement` holds info about arrangements in a worship."""
    q = (
        Arrangement.select(Arrangement, Person, Role)
        .join_from(Arrangement, Person)
        .join_from(Arrangement, Role)
        .join_from(Arrangement, WorshipArrangement)
        .join_from(WorshipArrangement, Worship)
        .where(Worship.date == datetime.date(2019, 1, 1))
    )
    assert [f"{e.role.name}: {e.person.name}" for e in q] == [
        f"Role {i}: Person {i}" for i in range(1, 4)
    ]
