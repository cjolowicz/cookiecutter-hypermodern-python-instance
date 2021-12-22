"""Sphinx configuration."""
from datetime import datetime


project = "Cookiecutter Hypermodern Python Instance"
author = "Claudio Jolowicz"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
]
autodoc_typehints = "description"
html_theme = "furo"
# workaround for bug: https://github.com/sphinx-doc/sphinx/issues/9383
linkcheck_ignore = [
    "codeofconduct.html",
    "contributing.html",
    "usage.html",
]
