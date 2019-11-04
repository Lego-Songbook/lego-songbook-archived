from typing import Type, Union

from .models import (
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
)

__all__ = ("Model",)

Model = Type[
    Union[
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
]
