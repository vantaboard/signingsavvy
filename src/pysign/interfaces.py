"""Module for providing data classes across the API."""

from dataclasses import dataclass


@dataclass
class Word:
    """Creates a word data class as an interface.

    Args:
        _id (int): ID used in remote URI.
        synoynm_id (int): ID for synonyms.
        name (str): Word name.
        usage (str): Example of word use.

    Attributes:
        _id (int): ID used in remote URI.
        synoynm_id (int): ID for synonyms.
        name (str): Word name.
        usage (str): Example of word use.

    """

    _id: int
    synonym_id: str
    name: str
    usage: str

    def __init__(self, _id: int, synonym_id: str, name: str, usage: str):
        self._id = _id
        self.synonym_id = synonym_id
        self.name = name
        self.usage = usage


@dataclass
class Variant:
    """Creates a variant data class as an interface.

    Args:
        _id (int): ID for the word variant.
        uri (str): Remote URI for word variant.
        vidld (str): Remote URI for 360p video.
        vidsd (str): Remote URI for 540p video.
        vidhd (str): Remote URI for 720p video.
        index (int): Index used in remote URI.
        type (str): Sign type.
        desc (str): Variant description.
        tip (str): Combined mnemonic and notice.
        word_id (int): Reference to the word.

    Attributes:
        uri (str): Remote URI for word variant.
        vidld (str): Remote URI for 360p video.
        vidsd (str): Remote URI for 540p video.
        vidhd (str): Remote URI for 720p video.
        index (int): Index used in remote URI.
        type (str): Sign type.
        desc (str): Variant description.
        tip (str): Combined mnemonic and notice.
        word_id (int): Reference to the word.

    """

    _id: int
    uri: str
    vidld: str
    vidsd: str
    vidhd: str
    _type: str
    desc: str
    tip: str
    word_id: int

    def __init__(
        self,
        _id: int,
        uri: str,
        vidld: str,
        vidsd: str,
        vidhd: str,
        _type: str,
        desc: str,
        tip: str,
        word_id: int,
    ):
        self._id = _id
        self.uri = uri
        self.vidld = vidld
        self.vidsd = vidsd
        self.vidhd = vidhd
        self.type = _type
        self.desc = desc
        self.tip = tip
        self.word_id = word_id


@dataclass
class WordList:
    """Creates a word list data class as an interface.

    Args:
        _id (int): ID of the word list.
        name (str): Name of the word list.
        word_id (int): Reference to the word.

    Attributes:
        _id (int): ID of the word list.
        name (str): Name of the word list.
        word_id (int): Reference to the word.

    """

    _id: int
    name: str
    word_id: int

    def __init__(self, _id: int, name: str, word_id: int):
        self._id = _id
        self.name = name
        self.word_id = word_id


@dataclass
class Sentence:
    """Creates a sentence data class as an interface.

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

    category: str
    sentence: str
    sentence_vidld: str
    sentence_vidsd: str
    sentence_vidhd: str

    def __init__(
        self, category, sentence,
        sentence_vidld, sentence_vidsd,
        sentence_vidhd
    ):
        self.category = category
        self.sentence = sentence
        self.sentence_vidld = sentence_vidld
        self.sentence_vidsd = sentence_vidsd
        self.sentence_vidhd = sentence_vidhd


@dataclass
class Article:
    """Creates an article data class as an interface.

    Args:
        id (int): ID used in remote URI.
        author_name (str): Full name of article author.
        date (str): Article date.
        html (str): Full HTML content for article.

    Attributes:
        id (int): ID used in remote URI.
        author_name (str): Full name of article author.
        date (str): Article date.
        html (str): Full HTML content for article.

    """

    _id: int
    author_name: str
    date: str
    html: str

    def __init__(self, _id: int, author_name: str, date: str, html: str):
        self._id = _id
        self.author_name = author_name
        self.date = date
        self.html = html
