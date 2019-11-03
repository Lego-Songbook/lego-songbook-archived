"""
Basic loading & dumping functions.

Dumping:

    Database => In-Stream => `dump()` => Out-Stream => File/Stdout

Loading:

    File/Stdin => In-Stream => `load()` => Out-Stream => Database

"""
from io import StringIO
from pathlib import Path
from typing import Sequence

import tablib

from songbook import models, types


def _dump_table(table: types.Model, directory: Path, format_: str):
    """Dump a single table."""
    table.select().tuples()
    table.fields()
    dataset = tablib.Dataset(*table.select().tuples(), headers=table.fields())

    if directory is not None:
        print(f"    Dumping {table.table_name()}...")
        out_file = Path(directory) / f"{table.table_name()}.{format_}"
        out_file.write_text(dataset.export(format_))
        print("    Done.")
        print("=====================")
    else:
        print(dataset.export(format_))


def _dump(table: types.Model, format_: str) -> str:
    table.select().tuples()
    table.fields()
    data = tablib.Dataset(*table.select().tuples(), headers=table.fields())
    return data.export(format_)


def _load(table: types.Model, in_stream: str, format_: str) -> int:
    data = tablib.Dataset(headers=table.fields()).load(in_stream, format=format_)
    return table.insert_many(data.dict).execute()


def _load_table(table: types.Model, directory: Path, format_: str):
    """Dump a single table."""

    if directory is not None:
        print(f"    Loading {table.table_name()}...")
        in_file = Path(directory) / f"{table.table_name()}.{format_}"
        dataset = tablib.Dataset(headers=table.fields()).load(in_file.read_text())
        print(f"    Importing {table.table_name()} into the database...")
        table.insert_many(dataset.dict).execute()
        print("    Done.")
        print("=====================")
    else:
        pass
        # print(dataset.export("csv"))


def dump(tables: Sequence[types.Model] = None, directory: str = None):
    """Dump the existing tables into csv files."""
    tables = tables or models.TABLES

    directory = Path(directory or "data/csv/").absolute()
    if not directory.exists():
        raise ValueError(f"{directory} is not a valid path.")
    print(f"Target directory: {directory}")
    for i, table in enumerate(tables):
        print(f"{i+1}. Processing {table.table_name()}...")
        print(f"    Fields: {table.fields()}")
        _dump_table(table=table, directory=directory, format_="csv")


def load(tables: Sequence[types.Model] = None, directory: str = None):
    """Load the existing csv files to the database."""
    tables = tables or models.TABLES
    directory = Path(directory or "data/csv/").absolute()
    if not directory.exists():
        raise ValueError(f"{directory} is not a valid path.")
    print(f"Target directory: {directory}")
    for i, table in enumerate(tables):
        print(f"{i+1}. Processing {table.table_name()}...")
        print(f"    Fields: {table.fields()}")
        _load_table(table=table, directory=directory, format_="csv")
