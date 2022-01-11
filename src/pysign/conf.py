# -- Path setup --------------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.abspath("../src"))


# -- Project information -----------------------------------------------------

project = "pysign"
copyright = "2022, Brighten Tompkins"
author = "Brighten Tompkins"


# -- General configuration ---------------------------------------------------

extensions = ["sphinx.ext.autodoc", "sphinx.ext.autosummary", "myst-parser"]

templates_path = ["_templates"]

exclude_patterns = []

autosummary_generate = True
autodoc_default_options = {
  "members": True,
  "inherited-members": True,
  "private-members": True,
  "show-inheritance": True,
}

# -- Options for HTML output -------------------------------------------------

html_theme = "renku"
