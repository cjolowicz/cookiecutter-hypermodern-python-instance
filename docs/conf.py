"""Sphinx configuration."""
project = "Cookiecutter Hypermodern Python Instance"
author = "Claudio Jolowicz"
copyright = "2022, Claudio Jolowicz"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
# workaround for bug: https://github.com/sphinx-doc/sphinx/issues/9383
linkcheck_ignore = [
    "codeofconduct.html",
    "contributing.html",
    "usage.html",
]
