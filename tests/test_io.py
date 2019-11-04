from io import StringIO

import pytest

import songbook.io
from songbook import models

ARRANGEMENT_CSV = """\
id,person_id,role_id
1,1,1
"""


ARTIST_CSV = """\
id,name
1,"Artist 1"
2,"Artist 2"
"""


@pytest.mark.usefixtures("test_clean_db")
def test_load():
    songbook.io.load(table=models.Artist, in_stream=StringIO(ARTIST_CSV), format_="csv")

    artist = models.Artist.get_by_id(2)
    assert artist.name == "Artist 2"


@pytest.mark.usefixtures("test_db")
def test_dump():
    data = songbook.io.dump(models.Artist, "csv")
    assert (
        data
        == """\
id,name\r
1,Artist 1\r
2,Artist 2\r
3,Artist 3\r
"""
    )
