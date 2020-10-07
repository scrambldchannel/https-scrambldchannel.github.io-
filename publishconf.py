#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = 'https://scrambldchannel.github.io'
SITELOGO = SITEURL + "/images/me_staring_into_the_trees.jpg"
RELATIVE_URLS = False

# this is breaking with one post, disabling until I get sort it out
# FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ALL_ATOM = None
# CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
CATEGORY_FEED_ATOM = None

DELETE_OUTPUT_DIRECTORY = True

