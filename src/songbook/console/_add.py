import datetime

import click

from ..models import Arrangement, Song, Worship


@click.group("add")
def add():
    pass


@add.command("song")
@click.option("-n", "--name", required=True)
@click.option("-k", "--key")
@click.option("-h", "--hymn")
def _add_song(name, key, hymn):
    print(f"Name: {name}, Key: {key}, Hymn No.: {hymn}.")
    song = Song.create(name=name)
    if key is not None:
        song.key = key
    if hymn is not None:
        song.hymn = hymn
    print(repr(song))
    song.save()
    return song


@add.command("arrangement")
@click.option("-n", "--name", required=True)
@click.option("-r", "--role", required=True)
def _add_arrangement(name, role):
    return Arrangement.create(name=name, role=role)


# Ways to add worships via a cliL
# 1. Use the id of songs & worships.
# 2. "get_or_create()".
# 3. songbook add worship -a "Keyboard, Adam" -a "Drums, Bella" -s "Song A" -s "Song B"
@add.command("worship")
@click.option("-d", "--date", required=True)
@click.option("-a", "--arrangements", nargs=2, multiple=True)
@click.option("-s", "--songs", multiple=True)
def _add_worship(date, arrangements, songs):  # TODO: How to add worships via a cli?
    arrangement_data = [
        Arrangement.get_or_create(role=arr[0], name=arr[1])[0] for arr in arrangements
    ]
    print(arrangement_data)
    song_data = [Song.get_or_create(name=song)[0] for song in songs]
    print(song_data)
    worship = Worship.create(date=datetime.date.fromisoformat(date))
    worship.arrangements.add(arrangement_data)
    worship.songs.add(song_data)
    print(repr(worship))
