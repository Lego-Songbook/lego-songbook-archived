from collections import OrderedDict
from datetime import date

import pytest

import sing

TEST_SONGS = [("Song A", "C", 335), ("Song B", "C#", 253), ("Song C", "Bb", 5)]
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
    sing.initialize(":memory:")
    assert sing.db.get_tables()
    assert sing.db.table_exists("song")
    assert sing.db.table_exists("arrangement")
    assert sing.db.table_exists("worship")


def test_add_songs():
    sing.add_songs(TEST_SONGS)
    song_a = sing.Song.get(sing.Song.name == "Song A")
    assert song_a.key == "C"
    assert song_a.hymn_ref is None


def test_add_conflicting_songs():
    sing.add_songs([("Song A", "Eb", None)])
    song = sing.Song.get(sing.Song.name == "Song A")
    assert song.key == "Eb"
    assert song.hymn_ref == 355
    assert song.id == 1


#
#
# def test_add_arrangements():
#     sing.add_arrangements(TEST_ARRANGEMENTS)
#     arrangement = sing.Arrangement.get(sing.Arrangement.role == "Keyboard", sing.Arrangement.name == "Adam")
#     assert arrangement.name == "Adam"
#     assert arrangement.role == "Keyboard"
#
#
# def test_add_existing_arrangements():
#     sing.add_arrangements({"Drums": "Fiona"})
#     arrangement = sing.Arrangement.get(sing.Arrangement.role == "Drums", sing.Arrangement.name == "Fiona")
#     assert arrangement.name == "Fiona"
#     assert arrangement.role == "Drums"


def test_add_worship():
    sing.add_worship(
        date=date(2019, 10, 6),
        songs=["Song B", "Song A"],
        arrangements={"Leader": "Adam", "Vocal": "Bella", "Keyboard": "Eliot"},
    )
    worship = sing.Worship.get(sing.Worship.date == date(2019, 10, 6))
    assert [song.name for song in worship.songs] == ["Song A", "Song B"]
    assert {x.role: x.name for x in worship.arrangements} == {
        "Leader": "Adam",
        "Vocal": "Bella",
        "Keyboard": "Eliot",
    }
