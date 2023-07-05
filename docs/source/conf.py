# -- Path setup --------------------------------------------------------------

import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, root_path)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'DatabankPy'
copyright = '2023 Douglas Neuroinformatics Platform'
author = 'Joshua Unrau'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx.ext.viewcode' ]

templates_path = ['_templates']
exclude_patterns = ['.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
html_css_files = ["custom.css"]

html_theme_options = {
    "repository_url": "https://github.com/DouglasNeuroInformatics/DatabankPy",
    "use_repository_button": True,
    "show_navbar_depth": 3
}

html_title = "DatabankPy"