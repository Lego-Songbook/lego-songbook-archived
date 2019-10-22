import click

from .database import add_songs, add_worship, initialize
from .models import db


@click.group()
def main():
    initialize("songbook.db")


@main.command()
@click.option("--table", prompt="Table name", help="the name of the table to show.")
@click.option("--first", default=10, help="show the first x entries of a table.")
def show(table, first):
    """Show the first x entries of the given table."""
    results = db.execute_sql(f"SELECT * FROM {table} LIMIT {first}")
    for result in results:
        print(result)


@main.command()
@click.option("--name", prompt="Name")
@click.option("--key", prompt="Key")
@click.option("--hymn", prompt="Hymn Ref")
def add_song(name, key, hymn):
    add_songs([(name, key, hymn)])
    print(f"{name} is added.")
