from collections import OrderedDict
from datetime import date

import pytest

from songbook import models
from songbook import database

TEST_SONGS = [("Song A", "C", None), ("Song B", "C#", 253), ("Song C", "Bb", 5)]
TEST_ARRANGEMENTS = OrderedDict(
    [
        ("Keyboard", "Adam"),
        ("Bass", "Bella"),
        ("Guitar", "Eliot"),
        ("Drums", "Fiona"),
        ("Leader", "Adam"),
        ("Guitar", "Fiona"),
    ]
)


def test_db_init():
    database.initialize(":memory:")
    assert database.db.get_tables()
    assert database.db.table_exists("song")
    assert database.db.table_exists("arrangement")
    assert database.db.table_exists("worship")


def test_add_songs():
    database.add_songs(TEST_SONGS)
    song_a = models.Song.get(models.Song.name == "Song A")
    assert song_a.key == "C"
    assert song_a.hymn_ref is None


def test_add_conflicting_songs():
    database.add_songs([("Song A", "Eb", 335)])
    song = models.Song.get(models.Song.name == "Song A")
    assert song.key == "Eb"
    assert song.hymn_ref == 335
    assert song.id == 1


def test_add_worship():
    database.add_worship(
        date=date(2019, 10, 6),
        songs=["Song B", "Song A"],
        arrangements={"Leader": "Adam", "Vocal": "Bella", "Keyboard": "Eliot"},
    )
    worship = models.Worship.get(models.Worship.date == date(2019, 10, 6))
    assert [song.name for song in worship.songs] == ["Song A", "Song B"]
    assert {x.role: x.name for x in worship.arrangements} == {
        "Leader": "Adam",
        "Vocal": "Bella",
        "Keyboard": "Eliot",
    }
