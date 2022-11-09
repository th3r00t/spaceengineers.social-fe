"""Configuration file for the Sphinx documentation builder."""
import os
import sys

sys.path.insert(0, os.path.abspath("../../"))
sys.path.insert(1, os.path.abspath("../../sesocial/"))
project = "SESocial Frontend & Api"
copyright = "2022, th3r00t"
author = "th3r00t"
version = "0.1"
release = "0.1.1 beta"
pygments_style = "sphinx"
todo_include_todos = True
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
show_authors = True


def setup(app):
    app.add_css_file("theme_overrides.css")


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# extensions = []
extensions = ["sphinx.ext.napoleon", "sphinx.ext.intersphinx", "myst_parser"]
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
napoleon_google_docstring = False
napoleon_user_param = False
napoleon_use_ivar = True
templates_path = ["_templates"]
# exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_logo = "../../static/images/logos/se_hires_logo_2_color_trans_bg.svg"
# html_theme = 'default'
html_static_path = ["_static", "../../static"]
