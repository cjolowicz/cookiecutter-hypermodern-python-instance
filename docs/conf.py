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
