# Configuration file for the Sphinx documentation builder.
# Al Mamun Oualid - Doctor Features Documentation

import os
import sys
sys.path.insert(0, os.path.abspath('../../..'))

# Project information
project = 'Medilink - Doctor Features'
copyright = '2025, Al Mamun Oualid'
author = 'Al Mamun Oualid'
release = '1.0.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# HTML output options
html_theme = 'alabaster'
html_static_path = ['_static']
html_theme_options = {
    'description': 'Documentation for Doctor Features (F3, F4, F5)',
    'github_user': 'mahtabthestranger',
    'github_repo': 'Medilink',
    'fixed_sidebar': True,
}

# Todo extension
todo_include_todos = True

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}
