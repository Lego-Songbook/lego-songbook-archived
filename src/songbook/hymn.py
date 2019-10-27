import requests
import tablib
from bs4 import BeautifulSoup

__all__ = ("get",)

_SITE = "http://sw.51christ.com/opern/index.php?from=singlemessage&isappinstalled=0"


def get(site=_SITE, output="db/csv/hymn.csv"):
    soup = BeautifulSoup(requests.get(site).content, "html.parser")

    hymn_data = [song.span.string.split(".") for song in soup.find_all("li")]

    hymn = tablib.Dataset(headers=["index", "name"])

    for song in hymn_data:
        hymn.append([int(song[0]), song[1]])

    with open(output, "w", newline="\n") as csv:
        csv.write(hymn.csv)
