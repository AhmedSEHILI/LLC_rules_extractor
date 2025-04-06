# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

project = 'LLCrulesExtractor'
copyright = '2025, SupGalileeING2'
author = 'SupGalileeING2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']

templates_path = ['_templates']
exclude_patterns = []

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_baseurl = '/'

html_theme_options = {
    "style_external_links": False,
}

html_static_path = ['_static']
html_css_files = []
html_js_files = []

html_copy_source = False
html_show_sourcelink = False
html_show_sphinx = False

html_context = {
    "display_github": False,
}

html_theme = 'classic' 

