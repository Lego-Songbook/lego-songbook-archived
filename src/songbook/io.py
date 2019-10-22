import os
import re
from typing import List, Tuple


def import_sheet_names(path: str) -> List[str]:
    """Given a path, return a list of valid sheet names."""
    sheets = os.scandir(path)
    return [x.name for x in sheets]


def process_sheet_name(sheet_name: str, format: str) -> Tuple[str]:
    """Given a sheet name and a format, return a tuple of splitted elements."""
