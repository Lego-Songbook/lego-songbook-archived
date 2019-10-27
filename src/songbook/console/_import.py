import os
from pathlib import Path

import click
import tablib

from ..models import Song, Arrangement, Worship, Hymn


_MODEL_NAMES = {
    "song": Song,
    "arrangement": Arrangement,
    "arr": Arrangement,
    "worship": Worship,
    "hymn": Hymn,
}


def _import_songs_from_folder(input_, delimiter, fields, conflict_action) -> int:
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


def _import_from_file(table, input_) -> int:
    model = _MODEL_NAMES[table]
    data = tablib.Dataset().load(open(input_, "r").read())
    return model.insert_many(data.dict).execute()


@click.command("import")
@click.argument("table")
@click.option("-i", "--input", "input_")
@click.option("-d", "--delimiter", default="-")
@click.option("--fields", default=(Song.key, Song.name))
@click.option("--update", "conflict_action", flag_value="update", default=True)
@click.option("--ignore", "conflict_action", flag_value="ignore")
def import_(table, input_, delimiter, fields, conflict_action):
    if table not in _MODEL_NAMES.keys():
        raise ValueError(f"Invalid table name: {table}.")
    if input_ is None:
        raise ValueError("Must specify a directory or a path to import via `--input`.")
    elif table == "song" and input_ is not None and Path(input_).is_dir():
        result = _import_songs_from_folder(
            input_=input_,
            delimiter=delimiter,
            fields=fields,
            conflict_action=conflict_action,
        )
    else:
        return _import_from_file(table=table, input_=input_)

    print(result)
