import click

from ..models import Song, Arrangement, Worship, Hymn


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


@view.command("arrangement")
def _view_arrangement():
    query = Arrangement.select().execute()
    for arr in query:
        print(repr(arr))


@view.command("worship")
def _view_worship():
    query = Worship.select().execute()
    for worship in query:
        print(repr(worship))


@view.command("hymn")
@click.option("-n", "--name")
@click.option("-i", "--index", type=int)
def _view_hymn(name, index):
    query = Hymn.select()
    if name is not None:
        query = query.where(Hymn.name.contains(name))
    if index is not None:
        query = query.where(Hymn.index == index)
    query = query.execute()
    for hymn in query:
        print(repr(hymn))
