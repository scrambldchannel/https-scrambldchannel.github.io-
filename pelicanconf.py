from datetime import datetime

AUTHOR = 'Alexander Sutcliffe'
SITEURL = 'http://localhost:8000'
SITENAME = 'scrambld notes'
SITETITLE = 'scrambld notes'
SITESUBTITLE = 'Feverish scribblings on all things TM1, Python and data'
SITELOGO = SITEURL + "/images/scrambldchannel.jpg"
#FAVICON = 'favicon.png'
BROWSER_COLOR = '#333'

CC_LICENSE = {
    "name": "Creative Commons Attribution-ShareAlike",
    "version": "4.0",
    "slug": "by-sa"
}

ROBOTS = 'index, follow'

THEME = 'theme/Flex-master'
PATH = 'content'

TIMEZONE = 'Europe/Berlin'

MARKUP = ('md', 'ipynb')
PLUGIN_PATHS = ['plugins']
IGNORE_FILES = [".ipynb_checkpoints"]  

I18N_TEMPLATES_LANG = 'en'
DEFAULT_LANG = 'en'
OG_LOCALE = 'en_GB'
LOCALE = 'en_GB'

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

USE_FOLDER_AS_CATEGORY = False
MAIN_MENU = True
HOME_HIDE_TAGS = True

MENUITEMS = [('About', '/pages/about.html'),
             ('Tags', '/tags.html'),]


SOCIAL = [ 
    ('github', 'https://github.com/scrambldchannel'),
    ('linkedin', 'https://www.linkedin.com/in/alexander-sutcliffe-b56921166/'),
    ('twitter', 'https://twitter.com/scrambldchannel'),
]

COPYRIGHT_YEAR = datetime.now().year
DEFAULT_PAGINATION = 10

GOOGLE_ANALYTICS = 'UA-161901975-1'

STATIC_PATHS = ['images']

THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True

USE_LESS = False
