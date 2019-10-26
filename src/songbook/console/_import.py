import os

import click

from .. import models


def _import_songs_from_folder(input_, delimiter, fields, conflict_action):
    song_data = []
    for sheet_file in os.scandir(input_):
        song_data.append(sheet_file.name.split(delimiter)[: len(fields)])
    return (
        models.Song.insert_many(song_data, fields=(models.Song.key, models.Song.name))
        .on_conflict(
            action=conflict_action,
            conflict_target=[models.Song.name],
            preserve=[models.Song.name],
        )
        .execute()
    )


def _import_songs_from_file(input_, format_):
    pass


def _import_songs(input_, format_, delimiter, fields, conflict_action):
    if format_ == "folder":
        _import_songs_from_folder(
            input_=input_,
            delimiter=delimiter,
            fields=fields,
            conflict_action=conflict_action,
        )
    else:
        _import_songs_from_file(input_, format_)


def _import_arrangements():
    pass


def _import_worships():
    pass


@click.command("import")
@click.argument("table")
@click.option("-f", "--format", "format_")
@click.option("-i", "--input", "input_")
@click.option("-d", "--delimiter", default="-")
@click.option("--fields", default=(models.Song.key, models.Song.name))
@click.option("--update", "conflict_action", flag_value="update", default=True)
@click.option("--ignore", "conflict_action", flag_value="ignore")
def import_(table, format_, input_, delimiter, fields, conflict_action):
    if table == "songs":
        _import_songs(
            input_=input_,
            format_=format_,
            delimiter=delimiter,
            fields=fields,
            conflict_action=conflict_action,
        )
    elif table == "arrangements":
        _import_arrangements()
    elif table == "worships":
        _import_worships()
    else:
        raise ValueError(f"Invalid table name {table}.")
