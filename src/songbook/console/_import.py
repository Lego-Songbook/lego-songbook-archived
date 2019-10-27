import os
from pathlib import Path

import click
import tablib

from ..models import Song, Arrangement, Worship, Hymn


_MODEL_NAMES = {
    "song": Song,
    "arrangement": Arrangement,
    "worship": Worship,
    "hymn": Hymn,
}


def _import_from_file(table, input_) -> int:
    model = _MODEL_NAMES[table]
    data = tablib.Dataset().load(open(input_, "r").read())
    return model.insert_many(data.dict).execute()


@click.group("import")
def import_():
    pass


# TODO: Importing songs from a dir seems like a one-off effort.
# TODO: Maybe I should just remove this for the sake of simplicity.
@import_.command("song")
@click.option("-i", "--input", "input_", required=True)
@click.option("-d", "--delimiter", default="-")
@click.option("--fields", default=(Song.key, Song.name))
@click.option("--update", "conflict_action", flag_value="update", default=True)
@click.option("--ignore", "conflict_action", flag_value="ignore")
def _import_song(input_, delimiter, fields, conflict_action):
    if Path(input_).is_dir():
        song_data = []
        for sheet_file in os.scandir(input_):
            song_data.append(sheet_file.name.split(delimiter)[: len(fields)])
        return (
            Song.insert_many(song_data, fields=(Song.key, Song.name))  # TODO: Use str
                .on_conflict(
                action=conflict_action,
                conflict_target=[Song.name],
                preserve=[Song.name],
            )
            .execute()
        )
    else:
        return _import_from_file(table="song", input_=input_)


@import_.command("arrangement")
@click.option("-i", "--input", "input_", required=True)
def _import_arrangement(input_):
    _import_from_file(table="arrangement", input_=input_)


@import_.command("worship")
@click.option("-i", "--input", "input_", required=True)
def _import_arrangement(input_):
    _import_from_file(table="worship", input_=input_)


@import_.command("hymn")
@click.option("-i", "--input", "input_", required=True)
def _import_arrangement(input_):
    _import_from_file(table="hymn", input_=input_)
