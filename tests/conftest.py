import datetime

import pytest
from peewee import SqliteDatabase

from songbook import models
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


@pytest.fixture
def test_clean_db():
    """Create a clean db for testing at the beginning of each test."""
    db = SqliteDatabase(":memory:")
    db.bind(models.TABLES)
    db.connect()
    db.create_tables(models.TABLES)
    yield db
    db.drop_tables(models.TABLES)
    db.close()


@pytest.fixture
def test_db():
    """Test db."""
    db = SqliteDatabase(":memory:")
    db.bind(models.TABLES)
    db.connect()
    db.create_tables(models.TABLES)

    Artist.insert_many(
        [(i, f"Artist {i}") for i in range(1, 4)], fields=[Artist.id, Artist.name]
    ).execute()

    Hymn.insert_many(
        [(i, f"Hymn {i}", i) for i in range(1, 4)],
        fields=[Hymn.id, Hymn.name, Hymn.key],
    ).execute()

    Key.insert_many(
        [(i, f"Key {i}") for i in range(1, 4)], fields=[Key.id, Key.name]
    ).execute()

    Person.insert_many(
        [(i, f"Person {i}") for i in range(1, 4)], fields=[Person.id, Person.name]
    ).execute()

    Role.insert_many(
        [(i, f"Role {i}") for i in range(1, 4)], fields=[Role.id, Role.name]
    ).execute()

    Arrangement.insert_many(
        [(i, i, i) for i in range(1, 4)],
        fields=[Arrangement.id, Arrangement.person, Arrangement.role],
    ).execute()

    Song.insert_many(
        [(i, f"Song {i}", i, i, i * 100, f"Scripture {i}") for i in range(1, 4)],
        fields=[Song.id, Song.name, Song.hymn, Song.artist, Song.tempo, Song.scripture],
    ).execute()

    Worship.insert_many(
        [(i, datetime.date(2019, i, 1)) for i in range(1, 4)],
        fields=[Worship.id, Worship.date],
    ).execute()

    WorshipSong.insert_many(
        [(i, 1, i) for i in range(1, 4)],
        fields=[WorshipSong.id, WorshipSong.worship, WorshipSong.song],
    ).execute()

    WorshipArrangement.insert_many(
        [(i, 1, i) for i in range(1, 4)],
        fields=[
            WorshipArrangement.id,
            WorshipArrangement.worship,
            WorshipArrangement.arrangement,
        ],
    ).execute()

    yield db

    db.drop_tables(models.TABLES)
    db.close()
