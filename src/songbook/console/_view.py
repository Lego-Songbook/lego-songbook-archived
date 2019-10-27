import click

from ..models import Song


@click.group("view")
def view():
    pass


@view.command("song")
@click.option("-l", "--limit", type=int, default=None)
@click.option("-k", "--key", type=str, default=None)
@click.option("-n", "--name", type=str, default=None)
def _view_song(limit, key, name):
    query = Song.select()
    if key:
        query = query.where(Song.key == key)
    if name:
        query = query.where(Song.name.contains(name))
    if limit:
        query = query.limit(limit)
    for song_ in query:
        print(repr(song_))
