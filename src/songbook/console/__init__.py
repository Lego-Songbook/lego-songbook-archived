"""
This module defines the command line behaviors.

Intended usage:

    $ songbook init  # builds the database from csv files.
    $ songbook sync  # make sure the db and the csv files are the same.

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
import os

import click

from .. import models
from ._add import add
from ._config import config
from ._export import export
from ._import import import_  # lol
from ._init import init
from ._remove import remove
from ._sync import sync
from ._update import update
from ._view import view


@click.group()
def main():
    models.init(os.environ.get("SONGBOOK_DB", "data/songbook.db"))


main.add_command(add)
main.add_command(config)
main.add_command(export)
main.add_command(import_)
main.add_command(init)
main.add_command(remove)
main.add_command(sync)
main.add_command(update)
main.add_command(view)
