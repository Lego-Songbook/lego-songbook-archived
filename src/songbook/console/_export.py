from pathlib import Path

import click
import tablib

from ..models import Arrangement, Hymn, Song, Worship, WorshipArrangement, WorshipSong


def _export(table, output, **kwargs):
    dataset = tablib.Dataset()
    dataset.headers = list(kwargs.keys())
    query = table.select(*kwargs.values()).tuples()
    for entry in query:
        dataset.append(entry)

    if output is not None:
        out_file = Path(output)
        out_file.write_text(dataset.export(out_file.suffix.strip(".")))
    else:
        print(dataset.export("csv"))


@click.group()
def export():
    pass


@export.command("song")
@click.option("-o", "--output")
def _export_song(output):
    _export(Song, output, id=Song.id, name=Song.name, key=Song.key, hymn=Song.hymn_id)


@export.command("arrangement")
@click.option("-o", "--output")
def _export_arrangement(output):
    _export(
        Arrangement,
        output,
        id=Arrangement.id,
        name=Arrangement.person,
        role=Arrangement.role,
    )


@export.command("worship")
@click.option("-o", "--output")
def _export_worship(output):
    _export(Worship, output, id=Worship.id, date=Worship.date)


@export.command("hymn")
@click.option("-o", "--output")
def _export_hymn(output):
    _export(Hymn, output, id=Hymn.id, name=Hymn.name, key=Hymn.key)
