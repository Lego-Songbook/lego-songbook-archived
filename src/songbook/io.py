"""
Basic loading & dumping functions.

Dumping:

    Database => In-Stream => `dump()` => Out-Stream => File/Stdout

Loading:

    File/Stdin => In-Stream => `load()` => Out-Stream => Database

"""
from io import StringIO

import tablib

from songbook import types


def dump(table: types.Model, format_: str) -> str:
    """Export a table into a desired format."""
    table.select().tuples()
    table.fields()
    data = tablib.Dataset(*table.select().tuples(), headers=table.fields())
    return StringIO(data.export(format_), newline="").read()


def load(table: types.Model, in_stream: StringIO, format_: str) -> int:
    """Load in-stream data into the database.

    Return the number of inserts.
    """
    data = tablib.Dataset(headers=table.fields()).load(in_stream.read(), format=format_)
    return table.insert_many(data.dict).execute()
