import click

from ..models import Song, Arrangement


def _add_song(name, key, hymn):
    if name is None or key is None:
        raise ValueError("Must specify the name and the key of the song!")
    song = Song.create(name=name, key=key)
    if hymn is not None:
        song.hymn = hymn
    song.save()
    return song


def _add_arrangement(name, role):
    if name is None or role is None:
        raise ValueError("Must specify the name and the role of the arrangement!")
    return Arrangement.create(name=name, role=role)


def _add_worship(date, arrangement, songs):
    if date is None:
        raise ValueError("Must specify the date of the worship!")


@click.command("add")
@click.argument("table")
@click.option("--name")
@click.option("--key")
@click.option("--hymn")
@click.option("--role")
def add(table, name, key, hymn, role):
    if table == "song":
        return _add_song(name=name, key=key, hymn=hymn)
    elif table == "arrangement":
        return _add_arrangement(name=name, role=role)
