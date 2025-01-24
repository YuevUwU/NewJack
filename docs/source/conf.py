# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'NewJack'
copyright = '2025, NewJack Developers'
author = 'NewJack Developers'

version = '0.1.0'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.duration",
    'sphinx.ext.githubpages',
    'sphinx.ext.graphviz',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinxcontrib.inkscapeconverter',
    'sphinx_togglebutton',
    'sphinxcontrib.youtube',
    'sphinx_design',
    'sphinx_tabs.tabs',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'zh_TW'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']
html_theme_options = {
    "repository_url": "https://github.com/su2u4-1/NewJack",
    "use_source_button": True,
    "repository_branch": "main",
    "use_edit_page_button": True,
    "use_repository_button": True,
    "use_issues_button": True
}

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True
