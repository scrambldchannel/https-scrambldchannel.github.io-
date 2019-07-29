#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Alexander'
SITENAME = 'Scrambld Notations'
SITEURL = 'https://scrambldchannel.github.io'

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
LINKS = (('Pelican', 'http://getpelican.com/'))
# Social widget

DEFAULT_PAGINATION = 10

# Theming
THEME = 'themes/nice-blog'
THEME_COLOR = 'gray'

SIDEBAR_DISPLAY = ['about', 'tags']
SIDEBAR_ABOUT = "Random musings on things like TM1, Python, data and stuff"
COPYRIGHT = "Alexander Sutcliffe "

# Plugins
PLUGIN_PATHS=['pelican-plugins','plugins']
#PLUGINS=['liquid_tags.notebook','ipynb.liquid',]


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True