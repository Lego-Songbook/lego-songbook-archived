from typing import Union

from .models import *

__all__ = ("Models",)

Models = Union[
    Arrangement,
    Artist,
    Hymn,
    Key,
    Person,
    Role,
    Song,
    Worship,
    WorshipArrangement,
    WorshipSong,
]
