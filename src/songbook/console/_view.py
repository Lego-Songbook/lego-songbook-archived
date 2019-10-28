import click

from ..models import Arrangement, Hymn, Song, Worship


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
@click.option("-d", "--date")
@click.option("-r", "--recent", type=int)
def _view_worship(date, recent):
    query = Worship.select()
    if date is not None:
        query = query.where(Worship.date == date)
    if recent is not None:
        query = query.order_by(Worship.date.desc()).limit(recent)
    query = query.execute()
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
