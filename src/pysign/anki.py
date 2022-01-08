"""Module is used for establishing a connection to Anki

Establishes a connection to Anki via AnkiConnect and creates
appropriate cards by selecting data from the database.

"""

import json
import logging
import re
import urllib

from logging import basicConfig
from typing import Any
from urllib.request import Request
from urllib.request import urlopen

from pick import pick
from sqlalchemy import select
from sqlalchemy.orm import Session as SQLSession

from pysign import db
from pysign.interfaces import Sentence
from pysign.interfaces import Variant
from pysign.interfaces import Word
from pysign.interfaces import WordList
from pysign.types import VideoQuality


basicConfig(
    filename="../../logs/pysign.log",
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} \
%(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    encoding="utf-8",
    level=logging.INFO,
)


def request(action, **params):
    return {"action": action, "params": params, "version": 6}


def invoke(action, **params):
    base = "http://localhost:8765"
    req = json.dumps(request(action, **params)).encode("utf-8")
    _open = urlopen(Request(base, req))

    res = json.load(_open)
    if len(res) != 2:
        raise Exception("Unexpected number of fields.")
    if "error" not in res:
        raise Exception("Missing required error field.")
    if "result" not in res:
        raise Exception("Missing required result field.")
    if res["error"] is not None:
        raise Exception(res["error"])
    return res["result"]


deckBase = "nonfiction::asl"
deckWords = f"{deckBase}::words"
deckSentences = f"{deckBase}::sentences"


def constructWord(word):
    return Word(
        word_id=word.word_id,
        synonym_id=word.synonym_id,
        word_name=word.word_name,
        word_usage=word.word_usage,
    )


def constructVariant(variant):
    return Variant(
        variant_uri=variant.variant_uri,
        variant_vidld=variant.variant_vidld,
        variant_vidsd=variant.variant_vidsd,
        variant_vidhd=variant.variant_vidhd,
        variant_index=variant.variant_index,
        variant_desc=variant.variant_desc,
        variant_tip=variant.variant_tip,
        word_id=variant.word_id,
    )


def constructWordLists(wordLists):
    wordListsToReturn = []
    for entry in wordLists:
        wordListsToReturn.append(
            WordList(
                word_list_id=entry.word_list_id,
                word_list_name=entry.word_list_name,
                word_id=entry.word_id,
            )
        )

    return wordListsToReturn


def constructSentence(sentence) -> Sentence:
    return Sentence(
        sentence_id=sentence.sentence_id,
        sentence=sentence.sentence,
        sentence_vidld=sentence.sentence_vidld,
        sentence_vidsd=sentence.sentence_vidsd,
        sentence_vidhd=sentence.sentence_vidhd,
    )


class Note:
    options: dict
    word: Word
    variant: Variant
    wordLists: Any
    sentence: Sentence

    def __init__(self, options: dict):
        self.options = options

    def getOptions(self) -> dict:
        return self.options

    def setWord(self, word):
        self.word = constructWord(word)

    def getWord(self) -> Word:
        return self.word

    def setVariant(self, variant):
        self.variant = constructVariant(variant)

    def getVariant(self) -> Variant:
        return self.variant

    def setWordLists(self, wordLists):
        self.wordLists = constructWordLists(wordLists)

    def getWordLists(self):
        return self.wordLists

    def setSentence(self, sentence):
        self.sentence = constructSentence(sentence)

    def getSentence(self) -> Sentence:
        return self.sentence


def addWordNote(note: Note, hq: VideoQuality):
    logging.info("Adding word note...")
    logging.info(note)

    (options, word, variant, wordLists) = (
        note.getOptions(),
        note.getWord(),
        note.getVariant(),
        note.getWordLists(),
    )

    wordListTags = []
    for wordList in wordLists:
        name = wordList.word_list_name
        fname = re.sub(r"\s", "-", name.lower())
        _id = wordList.word_list_id

        wordListTags.append(f"asl::wordlist::{fname}::{_id}")

    vid_url = variant[f"variant_vid{hq}"]

    res = invoke(
        "addNote",
        deckName=deckWords,
        modelName="basic_reverse_extra",
        fields={
            "Front": f"{word.name}: Variant {variant.variant_index}",
            "Back": "",
            "Extra": f"""
            {variant.variant_desc}
            {word.word_usage}
            """,
            "Source": f"{variant.variant_uri}",
            "Mind": f"{variant.variant_tip}",
        },
        options=options,
        tags=[
            f"asl::synonym-id::{word.synonym_id}",
            f"asl::word-id::{word.word_id}{variant.variant_index}",
        ]
        + wordListTags,
        video=[
            {
                "url": f"{vid_url}",
                "filename": f"asl-word-{word.word_id} \
                    {variant.variant_index}.mp4",
                "fields": ["Back"],
            }
        ],
    )

    logging.info(res)


def addSentenceNote(note: Note, hq: VideoQuality):
    logging.info("Adding sentence note...")
    logging.info(note)

    (options, sentence) = (
        note.getOptions(),
        note.getSentence(),
    )

    vid_url = sentence[f"sentence_vid{hq}"]

    res = invoke(
        "addNote",
        deckName=deckSentences,
        modelName="basic_reverse_extra",
        fields={
            "Front": f"{sentence.sentence}",
            "Back": "",
            "Extra": f"Category: {sentence.category}",
            "Source": "",
            "Mind": "",
        },
        options=options,
        tags=[f"asl::sentence-id::{sentence.sentence_id}"],
        video=[
            {
                "url": f"{vid_url}",
                "filename": f"asl-sentence-{sentence.sentence_id}.mp4",
                "fields": ["Back"],
            }
        ],
    )

    logging.info(res)


def fetchWordLists(note: Note, sqls: SQLSession) -> None:
    note.SetWordLists(
        sqls.execute(
            select(db.WordList).Where(
                db.WordList.word_id == note.getWord().word_id
            )
        )
        .scalars()
        .all()
    )


def addVariants(note: Note):
    for entry in select(db.Variant).Where(
        db.Variant.word_id == note.getWord().word_id
    ):
        note.setVariant(entry)


def addAllSentences(options, sqls: SQLSession, hq: VideoQuality):
    logging.info("Adding all sentences.")

    note = Note(options)

    sentences = sqls.query(db.Sentence)

    for entry in sentences:
        note.setWord(entry)
        fetchWordLists(note, sqls)
        addVariants(note)
        addSentenceNote(note, hq)


def addAllWords(options, sqls: SQLSession, hq: VideoQuality):
    logging.info("Adding all words.")

    note = Note(options)

    words = sqls.query(db.Word)

    for entry in words:
        note.setWord(entry)
        fetchWordLists(note)
        addVariants(note)
        addWordNote(note, hq)


def createDecks():
    deckNames = invoke("deckNames")
    for deck in [deckWords, deckSentences]:
        try:
            if deck in deckNames:
                raise FileExistsError

            logging.info(f"Creating {deck}")
            invoke("createDeck", deck=deck)
        except FileExistsError:
            logging.warning(f"Failed to create {deck}. Already exists.")


def deleteDecks():
    invoke("deleteDecks", decks=[deckWords, deckSentences])


def init():
    def options(deckName):
        return {
            "allowDuplicate": False,
            "duplicateScope": "deck",
            "duplicateScopeOptions": {
                "deckName": deckName,
                "checkChildren": False,
                "checkAllmodels": False,
            },
        }

    try:
        logging.info("Creating decks...")
        createDecks()

        logging.info("Establishing connection to database.")
        engine = db.connect()
        sqls = db.create_session(engine)

        logging.info("Prompting user for preferred video quality...")
        hqs = ["hd", "sd", "ld"]
        option, index = pick(
            ["720p", "540p", "360p"], "=== Pick a video quality ==="
        )

        addAllWords(options(deckWords), sqls, hqs[index])
        addAllSentences(options(deckSentences), sqls, hqs[index])
    except urllib.error.URLError:
        logging.error(
            "Connection refused. Is Anki open and Anki Connect installed?"
        )


init()
