from pathlib import Path


import click
import tablib

from ..models import Song, Hymn, Worship, Arrangement


def _export_table():
    pass


@click.group()
def export():
    pass


@export.command("song")
@click.option("-o", "--output")
def _export_song(output):
    out_file = Path(output)
    dataset = tablib.Dataset()
    dataset.headers = ["id", "name", "key", "hymn"]
    query = Song.select(Song.id, Song.name, Song.key, Song.hymn_id).tuples()
    for entry in query:
        dataset.append(entry)
    out_file.write_text(dataset.export(out_file.suffix.strip(".")), encoding="utf-8", newline="\n")


@export.command("arrangement")
def _export_arrangement():
    pass


@export.command("worship")
def _export_worship():
    pass


@export.command("hymn")
@click.option("-o", "--output")
def _export_hymn(output):
    out_file = Path(output)
    dataset = tablib.Dataset()
    dataset.headers = ["index", "name"]
    query = Hymn.select(Hymn.index, Hymn.name).tuples()
    for entry in query:
        dataset.append(entry)
    out_file.write_text(dataset.export(out_file.suffix.strip(".")))
