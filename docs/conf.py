"""Sphinx configuration."""
project = "Cookiecutter Hypermodern Python Instance"
author = "Claudio Jolowicz"
copyright = "2022, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
]
autodoc_typehints = "description"
html_theme = "furo"
