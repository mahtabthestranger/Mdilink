

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information ----------------
project = 'Patient Authentication Module'
copyright = '2024, Mahtab Ahmed'
author = 'Mahtab Ahmed'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Extension configuration -------------------------------------------------
autodoc_mock_imports = ['flask', 'flask_mysqldb', 'pymysql', 'werkzeug', 'config', 'models']

