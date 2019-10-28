import click


@click.group()
def remove():
    pass


@remove.command("song")
def _remove_song():
    pass


@remove.command("arrangement")
def _remove_arrangement():
    pass


@remove.command("worship")
def _remove_worship():
    pass


@remove.command("hymn")
def _remove_hymn():
    pass
