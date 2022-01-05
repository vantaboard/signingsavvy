"""This module is used for connecting to
and creating the database for pySign
"""

try:
    import curses
except ImportError:
    print("Curses failed to import.")

import logging

from getpass import getpass
from os import path

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


base = declarative_base()


def authenticate() -> tuple[str, str]:
    """Authenticates a user through a call to fetch_creds.

    Returns:
        Email and password from fetch_creds

    """

    return fetch_creds(curses.initscr())


def fetch_creds(stdscr) -> tuple[str, str]:
    """Fetches user credentials.

    Note:
        Makes use of the curses package for console interaction.

    Args:
        stdscr: Window object representing the entire screen.

    Returns:
        Email address and password.

    """

    logging.info("Authenticating user...")

    # Clear the window and allow echoing
    stdscr.clear()
    curses.echo()

    email = ""
    pw = ""

    # Prompt the user for their email address and password
    stdscr.addstr(0, 0, "=== Authenticate yourself ===")
    stdscr.addstr(1, 0, "Email: ")

    try:
        stdscr(email="utf-8").decode().getstr()
    except ValueError:
        logging.critical(
            "Failed to retrieve email address; \
                          defaulting to none."
        )

    try:
        pw = getpass("Password: ", None)
    except ValueError:
        logging.critical("Failed to retrieve password; defaulting to none.")

    return (email, pw)


class User(base):
    """Creates a user table using SQLAlchemy.

    Note:
        Not required if user does not wish to have access
        to extra fields or mature signs and some word lists.

    Args:
        user_email (str): SigningSavvy email address.
        user_pass (str): SigningSavvy password.

    Attributes:
        user_email (str): SigningSavvy email address.
        user_pass (str): SigningSavvy password.

    """

    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    user_email = Column(String, nullable=False)
    user_pass = Column(String, nullable=False)

    def __init__(self, user_email, user_pass):
        self.user_email = user_email
        self.user_pass = user_pass


class Word(base):
    """Creates a word table using SQLAlchemy.

    Args:
        word_id (int): ID used in remote URI.
        synoynm_id (int): ID for synonyms.
        word_name (str): Word name.
        word_usage (str): Example of word use.

    Attributes:
        word_id (int): ID used in remote URI.
        synoynm_id (int): ID for synonyms.
        word_name (str): Word name.
        word_usage (str): Example of word use.

    """

    __tablename__ = "word"

    word_id = Column(Integer, primary_key=True)
    synoynm_id = Column(Integer, nullable=False)
    word_name = Column(String, nullable=False)
    word_usage = Column(String)

    def __init__(self, word_id, synonym_id, name, usage):
        self.word_id = word_id
        self.synonym_id = synonym_id
        self.name = name
        self.usage = usage


class Variant(base):
    """Creates a variant table using SQLAlchemy.

    Args:
        variant_uri (str): Remote URI for word variant.
        variant_vidld (str): Remote URI for 360p video.
        variant_vidsd (str): Remote URI for 540p video.
        variant_vidhd (str): Remote URI for 720p video.
        variant_index (int): Index used in remote URI.
        variant_type (str): Sign type.
        variant_desc (str): Variant description.
        variant_tip (str): Combined mnemonic and notice.
        word_id (int): Reference to the word.

    Attributes:
        variant_uri (str): Remote URI for word variant.
        variant_vidld (str): Remote URI for 360p video.
        variant_vidsd (str): Remote URI for 540p video.
        variant_vidhd (str): Remote URI for 720p video.
        variant_index (int): Index used in remote URI.
        variant_type (str): Sign type.
        variant_desc (str): Variant description.
        variant_tip (str): Combined mnemonic and notice.
        word_id (int): Reference to the word.

    """

    __tablename__ = "variant"

    variant_id = Column(Integer, primary_key=True)
    variant_uri = Column(String, nullable=False)
    variant_vidld = Column(String, nullable=False)
    variant_vidsd = Column(String, nullable=False)
    variant_vidhd = Column(String, nullable=False)
    variant_index = Column(Integer, nullable=False)
    variant_type = Column(String)
    variant_desc = Column(String)
    variant_tip = Column(String)
    word_id = Column(Integer, ForeignKey("word.word_id"))

    def __init__(
        self,
        variant_uri,
        variant_vidld,
        variant_vidsd,
        variant_vidhd,
        variant_index,
        variant_type,
        variant_desc,
        variant_tip,
        word_id,
    ):
        self.variant_uri = variant_uri
        self.variant_vidld = variant_vidld
        self.variant_vidsd = variant_vidsd
        self.variant_vidhd = variant_vidhd
        self.variant_index = variant_index
        self.variant_type = variant_type
        self.variant_desc = variant_desc
        self.variant_tip = variant_tip
        self.word_id = word_id


class WordList(base):
    """Creates a word list table using SQLAlchemy.

    Args:
        word_list_id (int): ID used in remote URI.
        word_list_name (str): Name of the word list.
        word_id (int): Reference to the word.

    Attributes:
        word_list_id (int): ID used in remote URI.
        word_list_name (str): Name of the word list.
        word_id (int): Reference to the word.

    """

    __tablename__ = "wordlist"

    word_list_id = Column(Integer, primary_key=True)
    word_list_name = Column(String)
    word_id = Column(Integer, ForeignKey("word.word_id"))

    def __init__(self, word_list_id, word_list_name, word_id):
        self.word_list_id = word_list_id
        self.word_list_name = word_list_name
        self.word_id = word_id


class Sentence(base):
    """Creates a sentence table using SQLAlchemy.

    Args:
        category (str): Category of the sentence.
        sentence (str): Sentence.
        sentence_vidld (str): Remote URI for 360p video.
        sentence_vidsd (str): Remote URI for 540p video.
        sentence_vidhd (str): Remote URI for 720p video.

    Attributes:
        category (str): Category of the sentence.
        sentence (str): Sentence.
        sentence_vidld (str): Remote URI for 360p video.
        sentence_vidsd (str): Remote URI for 540p video.
        sentence_vidhd (str): Remote URI for 720p video.

    """

    __tablename__ = "sentence"

    sentence_id = Column(Integer, primary_key=True)
    category = Column(String)
    sentence = Column(String)
    sentence_vidld = Column(String)
    sentence_vidsd = Column(String)
    sentence_vidhd = Column(String)

    def __init__(
        self, category,
        sentence, sentence_vidld,
        sentence_vidsd, sentence_vidhd
    ):
        self.category = category
        self.sentence = sentence
        self.sentence_vidld = sentence_vidld
        self.sentence_vidsd = sentence_vidsd
        self.sentence_vidhd = sentence_vidhd


class Article(base):
    """Creates an article table using SQLAlchemy.

    Args:
        article_id (int): ID used in remote URI.
        author_name (str): Full name of article author.
        date (str): Article date.
        html (str): Full HTML content for article.

    Attributes:
        article_id (int): ID used in remote URI.
        author_name (str): Full name of article author.
        date (str): Article date.
        html (str): Full HTML content for article.

    """

    __tablename__ = "article"

    article_id = Column(Integer, primary_key=True)
    author_name = Column(String)
    date = Column(String)
    html = Column(String, nullable=False)

    def __init__(self, article_id, author_name, date, html):
        self.article_id = article_id
        self.author_name = author_name
        self.date = date
        self.html = html


def connect():
    """Initiate a connection to the SQLite database with SQLAlchemy.

    Returns:
        SQLAlchemy database engine linked to the db file or null.

    """

    logging.info("Connecting to database...")

    # Absolute path hack to get SQLAlchemy to create the engine
    p = path.abspath("../db/pysign.db3")
    engine = create_engine(f"sqlite:///{p}", future=True)

    return engine


def create_session(engine) -> Session:
    """Creates a database for use with `pysign`.

    Returns:
        engine: database engine

    """

    logging.info("Connecting to database...")

    base.metadata.create_all(engine)
    session = Session(engine)

    return session


def create_all(session: Session) -> None:
    """Uses a Session to create all of the data needed to fill the database."""
