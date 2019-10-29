import os

import click

from .. import models


@click.command()
def init():
    models.init(os.environ.get("SONGBOOK_DB", "data/songbook.db"))
