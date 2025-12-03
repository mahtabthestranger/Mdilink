


import os
import sys

sys.path.insert(0, os.path.abspath('../../'))

project = 'Medilink Admin Routes'
copyright = '2025, Medilink Development Team'
author = 'Medilink Development Team'
release = '1.0.0'
version = '1.0'

extensions = [
    'sphinx.ext.autodoc',          
    'sphinx.ext.viewcode',         
    'sphinx.ext.napoleon',         
    'sphinx.ext.intersphinx',      
    'sphinx.ext.todo',             
    'sphinx.ext.coverage',          
]

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'show-inheritance': True,
}

source_suffix = {
    '.rst': None,
}

master_doc = 'index'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = None
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
}

latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '10pt',
    'preamble': '',
    'figure_align': 'htbp',
}

latex_documents = [
    (master_doc, 'MedilinkAdminRoutes.tex', 'Medilink Admin Routes Documentation',
     'Medilink Development Team', 'manual'),
]

man_pages = [
    (master_doc, 'medilink-admin-routes', 'Medilink Admin Routes Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'MedilinkAdminRoutes', 'Medilink Admin Routes Documentation',
     author, 'MedilinkAdminRoutes', 'One line description of project.',
     'Miscellaneous'),
]

epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']

todo_include_todos = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'flask': ('https://flask.palletsprojects.com', None),
}

