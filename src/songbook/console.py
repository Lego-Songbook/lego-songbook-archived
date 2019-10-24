"""
This module defines the command line behaviors.

Intended usage:

    $ songbook init  # builds the database from csv files.
    $ songbook sync  # make sure the db and the csv files are the same.

    $ songbook import songs --format folder --input docs/assets/sheets/
    $ songbook export songs -f csv -o docs/_data/songs.csv [--update | --ignore]

    $ songbook config --db-uri db/songbook.db

    $ songbook view songs --limit 10 --key F
    $ songbook view songs --name "Song A"  # fuzzy match
    $ songbook view songs --date 2019-10-27

    $ songbook view worship --date 2019-10-27
    $ songbook view worship --recent 10
    $ songbook view worship --next-week

    $ songbook view arr --date 2019-10-27  # arrangements only

    $ songbook add song --name "Song A" --key "F#m" --hymn_ref 123
    $ songbook remove song --name "Song A"
    $ songbook remove song --key "C#" --all
    $ songbook update song --

"""


import click

from . import models


@click.group()
def main():
    models.init("db/songbook.db")


def _import_songs_from_folder(input_):
    pass


def _import_songs_from_file(format_, input_):
    pass


def _import_songs(format_, input_):
    if format_ == "folder":
        _import_songs_from_folder(input_)
    else:
        _import_songs_from_file(format_, input_)


def _import_arrangements():
    pass


def _import_worships():
    pass


@main.command("import")
@click.argument("table")
@click.option("-f", "--format")
@click.option("-i", "--input", "input_")
def import_(table, format_, input_):
    if table == "songs":
        _import_songs(format_, input_)
    elif table == "arrangements":
        _import_arrangements()
    elif table == "worships":
        _import_worships()
    else:
        raise ValueError(f"Invalid table name {table}.")


@main.command()
def export():
    pass


@main.command()
def config():
    pass


@main.command()
def view():
    pass


@main.command()
def sync():
    pass


@main.command()
def init():
    pass
