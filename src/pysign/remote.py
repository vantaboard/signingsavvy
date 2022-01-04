"""Module for connecting to the remote server

This module is used for attaching a connection
to act as an API for SigningSavvy.

"""

from bs4 import BeautifulSoup as soup
import logging

from sqlalchemy.orm import Session as SQLSession
from requests import Session as rSession
import requests
from sqlalchemy import select
from pysign import db
from pathlib import Path
import re

base = Path("https://www.signingsavvy.com")

def getPayload(s: SQLSession) -> dict:
  """Gets payload headers for the request session.

  Args:
    s: SQLSession for querying the database.

  Attributes:
    Email address and password.

  Returns:
    Dictionary containing header data.

  """

  logging.info("Fetching payload from database.")

  email = s.execute(select(db.User.user_email))
  pw = s.execute(select(db.User.user_pass))

  return {
    'action': 'login',
    'username': email,
    'password': pw,
    'login': 1,
    'search': '',
    'find': 1
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

  r = s.get(str(base / uri))
  html = soup(r.text, "html.parser")
  html.find_all("div.desc")[0].innerHTML.match("being signed")

  return html

def getHrefs(uri: str, query: str):
  """Generalized function for getting links.

  Args:
    query: HTML query to select links.

  Returns:
    links: Links specific to those being looked for.

  """

  html = getHTML(uri)

  logging.info(f"Using the {query} query on HTML.")

  links = html.find_all(query)

  hrefs = []
  for link in links:
      hrefs.append(link.href)

  return hrefs


def createWord(html: soup, uri: str):
  """Create a word through its insertion into the database.

  Args:
    html: HTML to pull word data from.
    uri: URI to pull additional word data from.

  """

  logging.info("Inserting word data from {uri} into database...")
  logging.info(f"Working off matches found from the {uri} for \
          VALUES of insertion.")

  # Regex on URI for word id.
  word_id_re = re.search(r"\d+(?=\/)(?<!\/)", uri)
  word_id = word_id_re.group[0]

  # Parsing HTML with BeautifulSoup.
  logging.info(f"Working off HTML data from the \
          {uri} for VALUES of insertion.")

  detail = Detail(html.find_all("div#tab-details"))
  word_name = detail.getDetail("fa-pencil")
  word_usage = detail.getDetail("fa-film")
  synonyms = detail.getDetail("fa-tags")

  variants = detail.tabDetails.find_all(".fa-cubes + div>ul>li>a").length - 1

  for index in range(variants):
    uri_without_variant = uri[-1]
    video_uri = html.find(".videocontent>link").href

    video_file_re = re.search(r"(?!\/)\d+(?=[\/.])", video_uri)
    video_group, video_id = word_id_re.group.[0:1]
    video_file_partial = f"{video_group}/{video_id}"

    variant_vidld = base / "media" / "mp4-ld" / f"{video_file_partial}.mp4"
    variant_vidsd = base / "media" / "mp4-sd" / f"{video_file_partial}.mp4"
    variant_vidhd = base / "media" / "mp4-hd" / f"{video_file_partial}.mp4"

    variant_type = detail.getDetail("fa-hand-paper-o")
    variant_desc = detail.getDetail("fa-info-circle")
    variant_aid = detail.getDetail("icon-eyeglasses")
    variant_notice = detail.getDetail("fa-exclamation-triangle")
    variant_tip = f"{variant_aid}\n{variant_notice}"

    uri = "{uri_without_variant}{index + 1}"
    html = getHTML(uri)
    detail = Detail(html.find_all("div#tab-details"))


class Detail():
    tabDetails:

  def __init__(self, html):
    self.tabDetails = html

  def getDetail(icon: str):
    return self.tab_details.find(f".{icon} + div>p").innerText ?? ""


def getWords():
  logging.info("Getting words from SigningSavvy")

  letterHrefs = getHrefs("search", "a.wlbutton")

  for href in letterHrefs:
    wordHrefs = getHrefs(href, "div.search_results>ul>li>a")

    for href in wordHrefs:
      createWord(href)

