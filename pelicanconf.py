from datetime import datetime

AUTHOR = 'Alexander Sutcliffe'
SITEURL = 'https://scrambldchannel.github.io'
SITENAME = 'Alexander''s Blog'
SITETITLE = 'Scrambld Notations'
SITESUBTITLE = 'Feverish scribblings on all things TM1, Python and data'
SITEDESCRIPTION = 'Feverish scribblings on all things TM1, Python and data'
SITELOGO = ''
FAVICON = '/images/favicon.ico'
BROWSER_COLOR = '#333333'
#PYGMENTS_STYLE = 'monokai'

ROBOTS = 'index, follow'

THEME = 'pelican-themes/Flex'
PATH = 'content'
#OUTPUT_PATH = 'blog/'
TIMEZONE = 'Europe/Berlin'

#I18N_TEMPLATES_LANG = 'en'
DEFAULT_LANG = 'en'
OG_LOCALE = 'en_UK'
LOCALE = 'en_UK'

#DATE_FORMATS = {
#    'en': '%B %d, %Y',
#}

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

USE_FOLDER_AS_CATEGORY = False
MAIN_MENU = True
HOME_HIDE_TAGS = True

SOCIAL = [ 
    ('github', 'https://github.com/scrambldchannel'),
    ('linkedin', 'https://www.linkedin.com/in/alexander-sutcliffe-b56921166/'),
]

GITHUB_URL = 'https://github.com/scrambldchannel'

MENUITEMS = [('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),]

#CC_LICENSE = {
#    'name': 'Creative Commons Attribution-ShareAlike',
#    'version': '4.0',
#    'slug': 'by-sa'
#}

COPYRIGHT_YEAR = datetime.now().year
DEFAULT_PAGINATION = 10

#DISQUS_SITENAME = "flex-pelican"
#ADD_THIS_ID = 'ra-55adbb025d4f7e55'

#STATIC_PATHS = ['images', 'extra']

CUSTOM_CSS = 'static/custom.css'

USE_LESS = False