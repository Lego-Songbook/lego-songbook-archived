import click

from ..models import Song, Arrangement


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
@click.option("--name", required=True)
@click.option("--role", required=True)
def _add_arrangement(name, role):
    return Arrangement.create(name=name, role=role)


# Ways to add worships via a cliL
# 1. Use the id of songs & worships.
# 2. "get_or_create()".
# 3. songbook add worship -a "Keyboard, Adam" -a "Drums, Bella" -s "Song A" -s "Song B"
@add.command("worship")
@click.option("--date", required=True)
@click.option("--arrangements")
@click.option("--songs")
def _add_worship(date, arrangements, songs):  # TODO: How to add worships via a cli?
    if date is None:
        raise ValueError("Must specify the date of the worship!")
