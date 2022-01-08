import logging

from logging import basicConfig
from os import makedirs
from pathlib import Path


basicConfig(
    filename="../../logs/pysign.log",
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} \
%(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    encoding="utf-8",
    level=logging.INFO,
)


def make_dirs() -> None:
    """Makes directories for pysign to use.

    Returns:
        No value.
    """

    # Create directories and handle file exists error.
    try:
        makedirs(Path("./db"))
        makedirs(Path("./assets/videos/words"))
        makedirs(Path("./assets/videos/sentences"))
        makedirs(Path("./assets/html/articles"))

    except FileExistsError:
        print("Warning: Some or all asset paths already exist.")


def make() -> None:
    """Calls other functions involved in starting pysign.

    Returns:
        No value.
    """

    make_dirs()
