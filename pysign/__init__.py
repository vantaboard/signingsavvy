"""This module demonstrates basic Sphinx usage with Python modules.

Submodules
==========

.. autosummary::
    :toctree: _autosummary

    anki
    api
    format
    start
"""

from .anki import *
from .api import *
from .format import *
from .start import *

__version__ = '0.0.1'
