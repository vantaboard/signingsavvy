import json
import logging
import re

from logging import basicConfig
from pathlib import Path

from bs4 import BeautifulSoup as soup
from flask import Flask
from requests import Session

from pysign.types import VideoQuality


s = Session()


app = Flask(__name__)


basicConfig(
    filename="../../logs/pysign.log",
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} \
%(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    encoding="utf-8",
    level=logging.INFO,
)


base = Path("https://www.signingsavvy.com")


def getHTML(uri: str):
    """Generalized function for getting html from a URI.

    Args:
        uri: URI to request from.

    Returns:
        html: The parsed HTML from the response text.

    """

    logging.info(f"Getting HTML from {uri}")

    r = s.get(uri)
    html = soup(r.text, "html.parser")

    return html


def IdFromURI(uri: str):
    regex = re.findall(r"\d+(?=\/)(?<!\/)", uri)
    return regex[0]


@app.route("/search/<sign>")
def search_api(sign: str):
    f = open("../tests/json/sign/4943_full_member.json")
    return json.load(f)


def fetchTabText(html: soup, classCSS: str):
    return html.select(f".{classCSS} + div>p")[0].innerText


def formatSignName(text: str):
    return re.findall(r"\w+(?=\s)", text)[0].title()


def formatSignLike(text: str):
    return re.findall(r"(?<=as in \").+(?=\")", text)[0]


def formatSignVideo(text: str):
    return re.findall(r"\d+\/\d+.mp4", text)[0]


def fetchSignSynonyms(html: soup):
    synonyms = []

    for _ in html.select(".fa-tags + div>ul>li>a"):
        synonyms.append(
            {
                "id": IdFromURI(_.href),
                "name": formatSignName(_.innerText),
                "like": formatSignLike(_.innerText),
            }
        )

    return synonyms


def fetchSignUsage(html: soup):
    usages = []

    text = map(
        lambda tag: tag.innerText, html.select(".fa-film + div>div>p")
    )

    values = []
    for i in range(text):
        values.append(text[i])

        if (i % 2 == 0):
            usages.append({
                "english": values[0],
                "asl": values[1],
            })

            values = []

    return usages


def fetchSignVariants(html: soup, name, sign):
    variants = []

    variantLen = html.find_all(".fa-cubes + div>ul>li>a").length + 1

    for i in range(variantLen):
        with getHTML(str(base / "sign" / name / sign / i)) as _:
            _type = fetchTabText(_, "fa-hand-paper-o")
            desc = fetchTabText(_, "fa-info-circle")
            aid = fetchTabText(_, "icon-eyeglasses")
            usage = fetchSignUsage(_)
            video = formatSignVideo(_.select("video")[0]["src"])

        variants.append(
            {
                "type": _type,
                "desc": desc,
                "aid": aid,
                "usage": usage,
                "video": video,
            }
        )

    return variants


@app.route("/sign/<sign>")
def sign_api(sign):
    with getHTML(str(base / "sign" / sign)) as _:
        name = fetchTabText(_, "fa-pencil")
        fname = formatSignName(name)
        flike = formatSignLike(name)
        synonyms = fetchSignSynonyms(_)
        variants = fetchSignVariants(_, name, sign)

    return {
        "id": sign,
        "name": fname,
        "like": flike,
        "synonyms": synonyms,
        "variants": variants,
    }


def getVideoLink(html: soup):
    uri = html.select(".videocontent>link")[0].href
    fileRegex = re.findall(r"(?!\/)\d+(?=[\/.])", str(uri))
    group, _id = fileRegex[0:1]
    return f"{group}/{_id}.mp4"
