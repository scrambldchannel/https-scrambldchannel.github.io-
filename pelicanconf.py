from datetime import datetime

AUTHOR = 'Alexander Sutcliffe'
SITEURL = 'http://localhost:8000'
SITENAME = 'scrambld notes'
SITETITLE = 'scrambld notes'
SITESUBTITLE = 'Feverish scribblings on all things TM1, Python and data'
BIO = 'Feverish scribblings on all things TM1, Python and data'
PROFILE_IMAGE = 'scrambldchannel.jpg'
#FAVICON = 'favicon.png'
BROWSER_COLOR = '#363636'

ROBOTS = 'index, follow'

THEME = 'theme/pelican-hyde-master'
PATH = 'content'

TIMEZONE = 'Europe/Berlin'

MARKUP = ('md', 'ipynb')
PLUGIN_PATHS = ['pelican-plugins']
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

USE_FOLDER_AS_CATEGORY = True
MAIN_MENU = True
HOME_HIDE_TAGS = True

SOCIAL = [ 
    ('github', 'https://github.com/scrambldchannel'),
    ('linkedin', 'https://www.linkedin.com/in/alexander-sutcliffe-b56921166/'),
    ('twitter', 'https://twitter.com/scrambldchannel'),
    ('instagram', 'https://www.instagram.com/scrambledchannel/'),
    ('flickr', 'https://www.flickr.com/bliix')
]

GITHUB_URL = 'https://github.com/scrambldchannel'

# Need to build support for this in theme
#MENUITEMS = [('About', '/pages/about.html'),
#             ('Tags', '/tags.html'),]

# Need to check whether these are relevant
COPYRIGHT_YEAR = datetime.now().year
DEFAULT_PAGINATION = 10

#DISQUS_SITENAME = "flex-pelican"
#ADD_THIS_ID = 'ra-55adbb025d4f7e55'

STATIC_PATHS = ['images']

USE_LESS = False
