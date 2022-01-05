"""Module for connecting to the remote server

This module is used for attaching a connection
to act as an API for SigningSavvy.

"""

import base64
import logging
import re

from pathlib import Path

import requests

from bs4 import BeautifulSoup as soup
from bs4 import select
from requests import Session as rSession
from sqlalchemy.orm import Session as SQLSession

from pysign import db
from pysign import interfaces


base = Path("https://www.signingsavvy.com")


def getPayload(sqls: SQLSession) -> dict:
    """Gets payload headers for the request session.

    Args:
        sqls: SQLSession for querying the database.

    Attributes:
        Email address and password.

    Returns:
        Dictionary containing header data.

    """

    logging.info("Fetching payload from database.")

    email = sqls.execute(select(db.User.user_email))
    pw = sqls.execute(select(db.User.user_pass))

    return {
        "action": "login",
        "username": email,
        "password": pw,
        "login": 1,
        "search": "",
        "find": 1,
    }


def connect() -> rSession:
    """Establishes a connection to SigningSavvy.

    Note:
    A request session is used to keep login information
    valid across multiple requests.

    Returns:
    session: Request session object with payload headers.

    """

    logging.info("Setting up request session...")

    engine = db.connect()
    session = requests.Session()
    payload = getPayload(db.create_session(engine))
    session.headers.update(payload)

    return session


s = connect()


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


def getHrefs(uri: str, query: str, base: bool = True):
    """Generalized function for getting links.

    Args:
        query: HTML query to select links.

    Returns:
        links: Links specific to those being looked for.

    """

    html = getHTML(str(base / uri) if base else uri)

    logging.info(f"Using the {query} query on HTML.")

    links = html.find_all(query)

    hrefs = []
    for link in links:
        hrefs.append(link.href)

    return hrefs


def getIdFromURI(uri: str):
    regex = re.findall(r"\d+(?=\/)(?<!\/)", uri)
    return regex[0]


def getArticleAuthor(html: soup):
    query = html.select(".blog-author")[0]
    formatted = re.sub(r"^BY\s", "", query).title()

    return formatted


def getArticleDate(html: soup):
    query = html.select(".blog-author-intro>p")[0].innerText
    regex = re.findall(r"(?!=\n).+", query)
    return regex[1]


def getSynonymId(synonyms: str):
    lower = synonyms.lower()
    formatted = re.sub(r"[^\w]", "", lower)
    bytesEncoded = str.encode(formatted)
    return base64.b64encode(bytesEncoded).decode()


def addWord(word: interfaces.Word, sqls: SQLSession):
    sqls.add_all(
        [
            db.Word(
                word_id=word.id,
                synonym_id=word.synonym_id,
                word_name=word.name,
                word_usage=word.usage,
            )
        ]
    )

    sqls.commit()


def addVariant(variant: interfaces.Variant, sqls: SQLSession):
    sqls.add_all(
        [
            db.Variant(
                variant_uri=variant.uri,
                variant_vidld=variant.vidld,
                variant_vidsd=variant.vidsd,
                variant_vidhd=variant.vidhd,
                variant_index=variant.index,
                variant_type=variant.type,
                variant_desc=variant.desc,
                variant_tip=variant.tip,
                word_id=variant.word_id,
            )
        ]
    )

    sqls.commit()


def addWordListEntry(wordList: interfaces.WordList, sqls: SQLSession):
    sqls.add_all(
        [
            db.WordList(
                word_list_id=wordList._id,
                word_list_name=wordList.name,
                word_id=wordList.word_id,
            )
        ]
    )

    sqls.commit()


def addSentence(sentence: interfaces.Sentence, sqls: SQLSession):
    sqls.add_all(
        [
            db.Sentence(
                category=sentence.category,
                sentence=sentence.sentence,
                desc=sentence.desc,
            )
        ]
    )

    sqls.commit()


def addArticle(article: interfaces.Article, sqls: SQLSession):
    sqls.add_all(
        [
            db.Article(
                article_id=article._id,
                author_name=article.author_name,
                date=article.date,
                html=article.html,
            )
        ]
    )

    sqls.commit()


class Detail:
    def __init__(self, html):
        self.tabDetails = html

    def getDetail(self, icon: str, inner=">p"):
        text = self.tabDetails.find(f".{icon} + div{inner}").innerText
        return text if text else ""


def getVideoLinks(html: soup):
    uri = html.select(".videocontent>link")[0].href
    fileRegex = re.findall(r"(?!\/)\d+(?=[\/.])", str(uri))
    group, _id = fileRegex[0:1]
    partial = f"{group}/{_id}"

    ld = base / "media" / "mp4-ld" / f"{partial}.mp4"
    sd = base / "media" / "mp4-sd" / f"{partial}.mp4"
    hd = base / "media" / "mp4-hd" / f"{partial}.mp4"

    return (ld, sd, hd)


def createVariant(
    uri: str,
    html: soup,
    _id: int,
    detail: Detail,
    sqls: SQLSession,
    word_id: int,
):
    uri_no_variant = uri[-1]

    vidld, vidsd, vidhd = getVideoLinks(html)

    _type = detail.getDetail("fa-hand-paper-o")
    desc = detail.getDetail("fa-info-circle")
    tip = f"""
    {detail.getDetail("icon-eyeglasses")}\n
    {detail.getDetail("fa-exclamation-triangle")}
    """
    uri = f"{uri_no_variant}{_id + 1}"

    logging.info("Inserting variant {variant_id} into table...")
    addVariant(
        interfaces.Variant(
            _id, uri, vidld, vidsd, vidhd, _type, desc, tip, word_id
        ),
        sqls,
    )

    html = getHTML(uri)


def createWord(html: soup, uri: str, sqls: SQLSession):
    """Create a word through its insertion into the database.

    Args:
    html: HTML to pull word data from.
    uri: URI to pull additional word data from.

    """

    # Regex on URI for word id.
    _id = getIdFromURI(uri)

    # Parsing HTML with BeautifulSoup.
    logging.info(
        f"Working off HTML data from the \
                {uri} for VALUES of insertion."
    )

    detail = Detail(html.find_all("div#tab-details"))

    name = detail.getDetail("fa-pencil")
    usage = detail.getDetail("fa-film")
    synonyms = detail.getDetail("fa-tags", "")

    addWord(interfaces.Word(_id, getSynonymId(synonyms), name, usage), sqls)

    variants = detail.tabDetails.find_all(".fa-cubes + div>ul>li>a").length - 1

    for index in range(variants):
        createVariant(uri, html, index, detail, s, _id)


def createWords():
    logging.info("Getting words from SigningSavvy")

    letterHrefs = getHrefs("search", "a.wlbutton")

    for href in letterHrefs:
        wordHrefs = getHrefs(href, "div.search_results>ul>li>a")

        for href in wordHrefs:
            createWord(href)


def getWordListItemId(uri: str):
    variantUris = getHrefs(uri, ".fa-cubes + div>ul>li>a", base=False)
    return getIdFromURI(variantUris[0])


def createWordLists():
    logging.info("Getting word lists from SigningSavvy")

    savvyHrefs = getHrefs("wordlist/savvy", ".mediumtext>a")

    for href in savvyHrefs:
        _id = getIdFromURI(href)

        r = s.get(href)
        html = soup(r.text, "html.parser")
        createSavvyWordList(html.select(".browselist-alphabetical"), _id, s)

    memberHrefs = getHrefs("wordlist/shared", ".mediumtext>a")

    for href in memberHrefs:
        _id = getIdFromURI(href)

        createMemberWordList(
            getHrefs(href, ".browselist-alphabetical>li>a"), _id, s
        )


def createSavvyWordList(htmlList: soup, _id, sqls: SQLSession):
    for i in range(htmlList):
        _id = int(f"{_id}{i}")
        name = htmlList[i].select("h3")
        items = htmlList[i].select(".browselist-alphabetical>li>a")

        for item in items:
            word_id = getWordListItemId(item.href)
            addWordListEntry(interfaces.WordList(_id, name, word_id), sqls)


def createMemberWordList(uris: list(str), _id: int, name, sqls: SQLSession):
    for uri in uris:
        word_id = getWordListItemId(uri)

        addWordListEntry(interfaces.WordList(_id, name, word_id), sqls)


def fetchSentenceCategoryHrefs():
    logging.info("Getting sentences from SigningSavvy")

    # Second phrase list is Sentences by Category
    uri = str(base / "sentences")
    r = s.get(uri)
    html = soup(r.text, "html.parser")
    query = html.select(".phrase_list")
    categoriesLinks = query.find_all("a")

    hrefs = []
    for link in categoriesLinks:
        hrefs.append(link.href)


def fetchSentenceLists(hrefs):
    categoryHrefs = fetchSentenceCategoryHrefs()

    for href in categoryHrefs:
        sentenceHrefs = getHrefs(href, "div>p>a", base=False)

        for href in sentenceHrefs:
            createSentence(href)


def createSentence(uri: str, sqls: SQLSession):
    r = s.get(uri)
    html = soup(r.text, "html.parser")

    category = html.select(".wordlist-bar>a")[0].innerText
    sentence = html.select(".signing_header")[0].innerText
    vidld, vidsd, vidhd = getVideoLinks(html)

    addSentence(
        interfaces.Sentence(category, sentence, vidld, vidsd, vidhd), sqls
    )


def createArticles():
    logging.info("Getting articles from SigningSavvy")

    pages = str(base / "article") + getHrefs(
        "article", ".blogpaging>.blogpage>a"
    )

    for page in pages:
        r = s.get(page)
        html = soup(r.text, "html.parser")
        articleLinks = html.select(".blog_blurb>.blog_summary>h3>a")

        for link in articleLinks:
            createArticle(link.href)


def createArticle(uri: str, sqls: SQLSession):
    logging.info(
        f"Working off HTML data from the \
                {uri} for VALUES of insertion."
    )

    r = s.get(uri)
    html = soup(r.text, "html.parser")

    _id = getIdFromURI(uri)
    author_name = getArticleAuthor(html)
    date = getArticleDate(html)

    addArticle(interfaces.Article(_id, author_name, date, html), sqls)
