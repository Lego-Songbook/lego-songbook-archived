import click


@click.group()
def update():
    pass


@update.command("song")
def _update_song():
    pass


@update.command("arrangement")
def _update_arrangement():
    pass


@update.command("worship")
def _update_worship():
    pass


@update.command("hymn")
def _update_hymn():
    pass
