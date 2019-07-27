#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Alexander'
SITENAME = 'Scrambld Notations'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Theming
THEME = 'themes/nice-blog'
THEME_COLOR = 'cyan'

SIDEBAR_DISPLAY = ['about', 'tags']
SIDEBAR_ABOUT = "Random musings on things like TM1, Python, data and stuff"
COPYRIGHT = "Alexander Sutcliffe "

# Plugins
PLUGIN_PATHS=['pelican-plugins','plugins']
#PLUGINS=['liquid_tags.notebook','ipynb.liquid',]


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True