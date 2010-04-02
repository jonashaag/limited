# coding: utf-8
from os import environ
from utils.utils import join_current_path
from django.template.defaultfilters import slugify

# Absolute URL to your blog
BLOG_URL = "http://localhost:8000/"

# Absolute path to the directory containing this settings file
BASE_DIR = '/home/jonas/www/watchthewatchers/limited/'
BASE_DIR = '/home/jonas/dev/projects/limited/'
join_current_path.BASE_DIR = BASE_DIR # DON'T delete this line

# Settings like blog title and keywords
DEFAULT_CONTEXT_VARIABLES = {
    'BLOG_TITLE' : 'My Funny Blog',
    # your blog main title
    'BLOG_SUBTITLE' : '...makes ponies fly',
    # your blog title (optional)
    'BLOG_KEYWORDS' : 'my, funny, tags',
    # keywords to be included in HTML meta tags
    'FEED_TITLE' : 'My Funny Blog Feed',
    # Title of your blog feed
}

# Database settings
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = join_current_path('%s.sql' %
                    slugify(DEFAULT_CONTEXT_VARIABLES['BLOG_TITLE']))
# (the following stuff is not required using sqlite)
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

# Your timezone and default language
TIME_ZONE = 'Europe/Berlin'
LANGUAGE_CODE = 'de-DE'
USE_I18N = True

# File upload directories
UPLOAD_DIRS = {
    'images' : 'upload/images',
    'files' : 'upload/files'
}

# MARKUP_PARSER =

USE_PYGMENTS = True

# Comment IP blacklist
IP_BLACKLIST = ()

# Comment word blacklist
WORD_BLACKLIST = (
    'xanax', 'viagra', '<b>', '<a href', 'meridia',
    'acyclovir', 'porn', 'adult', 'pharma',
)

# Widget configuration.
# The following three keys may be set and may have to following values:
#   'exclude':  a list or tuple of filenames to exclude or
#              'all' to exclude all widgets not listed in 'include'.
#
#   'include':  a list or tuple of filenames to include
#               (only used if 'exclude' is set to 'all'; order is relevant!)
#
#   'order':    a list or tuple of filenames defining the widget order
#               (only used if 'exclude' is not 'all').
#               Widgets that are included (either because they're listed in the
#               'include' list or because of automatical inclusion) but not
#               listed here will be added unsorted.
WIDGET_CONFIGURATION = {
    'exclude' : None,
    'include' : None,
    'order' : ('navigation_widget.html', 'rss_widget.html',
               'tag_widget.html', 'search_widget.html')
}

ENTRIES_PER_PAGE = 5
# posts displayed per page

# Path to media files
MEDIA_ROOT = join_current_path('media/')
# absolute path on your harddisk
MEDIA_URL = '/media/'
# relative url
ADMIN_MEDIA_PREFIX = '/admin_media/'
# relative url
ADMIN_URL = '/admin/'
# relative url

# Template paths (you shouldn't have to modify this)
TEMPLATE_PAGE = 'page.html'
TEMPLATE_BLOG = 'blog.html'
TEMPLATE_ARCHIVE = 'archive.html'
TEMPLATE_OVERVIEW_ARCHIVE = 'archive_overview.html'
TEMPLATE_FEED = 'feed.xml'
TEMPLATE_SEARCH = 'search.html'
USER_TEMPLATES_DIR = 'user_templates'
WIDGETS_DIR = 'widgets'

# Enable debugging?
DEBUG = True
TEMPLATE_DEBUG = True

# Admins and managers (name, email)
ADMINS = (
    ('Your Admin', 'admin@yourdomain.com'),
)
MANAGERS = ADMINS

LOGGING_OPTIONS = {
    'include_media' : False,
    'include_admin' : False
}


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'yoursecretkey'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.filesystem.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'limited.middlewares.log.LoggingMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'limited.urls'

TEMPLATE_DIRS = (
    join_current_path(USER_TEMPLATES_DIR),
    join_current_path('templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'limited.pages',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    #"limited.pages.make_request_context",
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
)
