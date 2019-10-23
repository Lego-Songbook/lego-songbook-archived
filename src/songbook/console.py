"""
This module defines the command line behaviors.

Intended usage:

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


def _import_songs_from_folder():
    pass


def _import_songs_from_file(format):
    pass


def _import_songs(format):
    if format == "folder":
        _import_songs_from_folder()
    else:
        _import_songs_from_file(format)


def _import_arrangements():
    pass


def _import_worships():
    pass


@main.command()
@click.option("-t", "--table")
@click.option("-f", "--format")
@click.option("-i", "--input", "input_")
def import_(table, format, input_):
    if table == "songs":
        _import_songs()
    elif table == "arrangements":
        _import_arrangements()
    elif table == "worships":
        _import_worships()
    pass


@main.command()
def export():
    pass


@main.command()
def config():
    pass


@main.command()
def view():
    pass



# @main.command()
# @click.option("--table", prompt="Table name", help="the name of the table to show.")
# @click.option("--first", default=10, help="show the first x entries of a table.")
# def show(table, first):
#     """Show the first x entries of the given table."""
#     results = db.execute_sql(f"SELECT * FROM {table} LIMIT {first}")
#     for result in results:
#         print(result)
#
#
# @main.command()
# @click.option("--name", prompt="Name")
# @click.option("--key", prompt="Key")
# @click.option("--hymn", prompt="Hymn Ref")
# def add_song(name, key, hymn):
#     add_songs([(name, key, hymn)])
#     print(f"{name} is added.")
#
#
# @main.command()
# @click.argument("table")
# @click.option("--")
# def import(table, path, ):
#     pass
