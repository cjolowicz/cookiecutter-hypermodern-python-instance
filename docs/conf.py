"""Sphinx configuration."""
from datetime import datetime

project = "Cookiecutter Hypermodern Python Instance"
author = "Claudio Jolowicz"
copyright = f"{datetime.now().year}, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
autodoc_typehints = "description"
