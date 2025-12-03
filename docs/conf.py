import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Medilink - Patient Authentication'
copyright = '2024, Mahtab Ahmed'
author = 'Mahtab Ahmed'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
autodoc_mock_imports = ['flask', 'flask_mysqldb', 'pymysql', 'werkzeug', 'dotenv']

templates_path = ['_templates']
exclude_patterns = ['_build']

html_theme = 'sphinx_rtd_theme'
