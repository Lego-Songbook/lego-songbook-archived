import click

from .. import models


def _view_songs(limit: int, key: str, name: str):
    query = models.Song.select()
    if key:
        query = query.where(models.Song.key == key)
    if name:
        query = query.where(models.Song.name.contains(name))
    if limit:
        query = query.limit(limit)
    for song in query:
        print(repr(song))


@click.command("view")
@click.argument("table")
@click.option("-l", "--limit", type=int, default=None)
@click.option("-k", "--key", type=str, default=None)
@click.option("-n", "--name", type=str, default=None)
def view(table, limit, key, name):
    if table == "songs":
        _view_songs(limit=limit, key=key, name=name)
