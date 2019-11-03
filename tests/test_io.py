import pytest

from songbook import io, models

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
    assert io._load(table=models.Artist, in_stream=ARTIST_CSV, format_="csv") == 2
