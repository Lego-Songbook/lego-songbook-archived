import click


@click.group()
def export():
    pass


@export.command("song")
def _export_song():
    pass


@export.command("arrangement")
def _export_arrangement():
    pass


@export.command("worship")
def _export_worship():
    pass


@export.command("hymn")
def _export_hymn():
    pass
