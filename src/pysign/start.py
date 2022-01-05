from pathlib import Path
from os import makedirs


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
