import click

from ..models import Song, Arrangement


@click.group("add")
def add():
    pass


@add.command("song")
@click.option("--name")
@click.option("--key")
@click.option("--hymn")
def _add_song(name, key, hymn):
    if name is None or key is None:
        raise ValueError("Must specify the name and the key of the song!")
    song = Song.create(name=name, key=key)
    if hymn is not None:
        song.hymn = hymn
    song.save()
    return song


@add.command("arrangement")
@click.option("--name")
@click.option("--role")
def _add_arrangement(name, role):
    if name is None or role is None:
        raise ValueError("Must specify the name and the role of the arrangement!")
    return Arrangement.create(name=name, role=role)


@add.command("worship")
@click.option("--arrangements")
@click.option("--songs")
def _add_worship(date, arrangements, songs):
    if date is None:
        raise ValueError("Must specify the date of the worship!")
