"""
Base version of the settings file.

Other settings files (local, test, etc.) 'inherit' from here by importing all
symbols from this file and then overwriting selected ones as needed.

"""

import os
#import djcelery
#djcelery.setup_loader()

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
# (taken from "Two Scoops of Django")
from django.core.exceptions import ImproperlyConfigured

_EC2_USER_DATA  = dict()
_USER_DATA_FILE = "/var/tmp/.__user_data"

def get_env_variable(var_name, default=None):
    """
    Get configuration parameters either from environment or EC2 user data.

    If we deploy on AWS EC2 then the user-data script should have written some values
    into the _USER_DATA_FILE location. There, they are formatted as key-value pairs,
    one per line, separated by '='. If the file is present then we take our value from
    there. Otherwise, we look in environment variables. If we don't find the value in
    either place we raise an exception.

    We use this to get values for sensitive settings, which should not be checked into
    the repository. Example: Secret keys and passwords. Also used for dynamically
    created values, such as the DB address.

    """
    # First check if we already have read the values from the user-data file.
    # Read and cache those values if the user-data file exists.
    if not _EC2_USER_DATA:
        # See if the user-data file exists.
        try:
            with open(_USER_DATA_FILE, "r") as f:
                for line in f.readlines():
                    try:
                        key,value = line.split("=", 1)
                        _EC2_USER_DATA[key.strip()] = value.strip()
                    except:
                        # Empty lines, comments, etc...
                        pass
        except IOError:
            # Looks like we are not running on EC2. So, ignore this and fall
            # through to getting the values from the environment.
            pass

    # Check if the variable exists in the cached user-data values.
    if var_name in _EC2_USER_DATA:
        return _EC2_USER_DATA[var_name]

    # If the variable name doesn't exist in user-data, we will fall through to checking
    # for it in the environment.
    try:
        return os.environ[var_name]
    except KeyError:
        if default:
            return default
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

#
# ----------------------------------------------------------------------------
# Project location and name.
# ----------------------------------------------------------------------------
#

PROJECT_DIR    = os.path.abspath(os.path.dirname(__file__)) + "/../"
PROJECT_NAME   = "ZZYYXX"

#
# ----------------------------------------------------------------------------
# Settings in the following session may/should be overwritten by
# the local settings file.
#
# The SITE... settings are for the server on which the Django app runs,
# while the CORP... settings are for the corporate home page.
# ----------------------------------------------------------------------------
#

SITE_DOMAIN        = "zzyyxx.com"
SITE_SERVER        = "www." + SITE_DOMAIN
SITE_URL           = "https://" + SITE_SERVER
CORP_SITE_DOMAIN   = "bar.com"
CORP_SITE_SERVER   = "www.bar.com"
CORP_SITE_URL      = "http://" + CORP_SITE_SERVER
COMPANY_NAME_SHORT = "ZZYYXX"
COMPANY_NAME_LONG  = "ZZYYXX Ltd."

LOGIN_REDIRECT_URL  = "/home/"
LOGIN_URL           = "/acc/login"

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# NOTE! Also see the definition of the SITES directory at the end of this file.


#
# ----------------------------------
# Miscellaneous settings
# ----------------------------------
#

SITE_ID = 1

# Make this unique, and don't share it with anybody.
SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY")

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'zzyyxx.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.twitter.TwitterBackend',
    'accounts.authentication.AuthBackend',
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
)

FIXTURE_DIRS        = [
    "fixtures",
]

ROOT_URLCONF        = 'zzyyxx.urls'
AUTH_USER_MODEL     = "accounts.UserModel"

# This is used in the accounts page to display the links and icons for
# social auths that are supported, but maybe not yet associated with the account.
SUPPORTED_SOCIAL_AUTHS = [
    {
        "name"       : "twitter",
        "human_name" : "Twitter",
        "icon"       : ""
    },
    {
        "name"       : "facebook",
        "human_name" : "Facebook",
        "icon"       : ""
    },
]

SUPPORTED_SOCIAL_AUTHS_BY_NAME = \
                        dict( [ (e['name'], e) for e in SUPPORTED_SOCIAL_AUTHS ] )

# I'll take care of any exceptions during social auth's processing myself"
# SOCIAL_AUTH_RAISE_EXCEPTIONS   = False
# SOCIAL_AUTH_PROCESS_EXCEPTIONS = 'accounts.views.process_social_auth_errors'

SOCIAL_AUTH_PIPELINE = (
    'accounts.views.custom_social_auth',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
)


#
# --------------------------------------
# Localization
# --------------------------------------
#

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

LANGUAGES = [
 ('de', 'German'),
 ('en', 'English'),
 ('en-gb', 'British English'),
]

DEFAULT_LANG = "en"

LOCALE_PATHS = (
    BASE_DIR+'../locale',
)

#
# --------------------------------------------------------------
# Directory locations and URLs for media and static files
# --------------------------------------------------------------
#

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = BASE_DIR+"static/uploaded/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/m/up/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/m/'

# Absolute path to the directory static files should be collected to.  Don't put
# anything in this directory yourself; store your static files in apps' "static/"
# subdirectories and in STATICFILES_DIRS.  Example:
# "/home/media/media.lawrence.com/static/"
#
# We append the STATIC_URL that appears as prefix for all static files in the URL,
# since it simplifies the serving of the static files (for example via uwsgi). The
# server just needs to check whether the request is for a static resource. If so, it
# can map the entire URL into the STATIC_ROOT directory, we don't have to strip off the
# STATIC_URL prefix.
#
STATIC_ROOT = 'STATIC_ROOT' + STATIC_URL

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_DIR+"../static/",
    PROJECT_DIR+"../static_thirdparty/bootstrap_2.2.2/",
    PROJECT_DIR+"../static_thirdparty/datatable/",
    PROJECT_DIR+"../static_thirdparty/tablesorter/",
    PROJECT_DIR+"../static_thirdparty/misc/",
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


#
# ---------------------------------------
# Templates
# ---------------------------------------
#

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"...
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_DIR + "../templates",
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

CORE_TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)

APP_TEMPLATE_CONTEXT_PROCESSORS = (
    "utils.context_processor.zzyyxx_context",
)

TEMPLATE_CONTEXT_PROCESSORS = CORE_TEMPLATE_CONTEXT_PROCESSORS + \
                              APP_TEMPLATE_CONTEXT_PROCESSORS


#
# ----------------------------------------
# Middleware
# ----------------------------------------
#

CORE_MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)


APP_MIDDLEWARE_CLASSES = (
    'accounts.middleware.TimezoneMiddleware',
)

MIDDLEWARE_CLASSES = CORE_MIDDLEWARE_CLASSES
MIDDLEWARE_CLASSES += APP_MIDDLEWARE_CLASSES

#
# ----------------------------------------
# Installed applications
# ----------------------------------------
#

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    # The 'accounts' app is one of ours, but we list it first,
    # since it contains the new user model, which may be referred
    # to by many other apps, including 3rd party apps.
    'accounts',
    # Some useful third-party apps
    'django_extensions',
    'south',
    #'djcelery',
    'social_auth',
    'crispy_forms',
    # The following are some more of our apps
    'utils',
    'check_js',
    'appcore',
    'toplevel',
    'mailprocessing',
    #'api',
)


#
# ------------------------------------
# Logging
# ------------------------------------
#

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(name)s: %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['console','mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
    'root': {
        'handlers':['console'],
        'level':'INFO'
    }
}



#
# -------------------------------------------------------------------------------------
# Sites once more, now that we have any possible definitions from the local settings.
# -------------------------------------------------------------------------------------
#

SITES = {
    "SITE_DOMAIN"      : SITE_DOMAIN,
    "SITE_SERVER"      : SITE_SERVER,
    "SITE_URL"         : SITE_URL,
    "CORP_SITE_DOMAIN" : CORP_SITE_DOMAIN,
    "CORP_SITE_SERVER" : CORP_SITE_SERVER,
    "CORP_SITE_URL"    : CORP_SITE_URL
}


#
# ------------------------------------
# Third party app settings
# ------------------------------------
#

#
# Social auth
#
TWITTER_CONSUMER_KEY                     = 'j6qQETDikjufq9jaGrdf1A'
TWITTER_CONSUMER_SECRET                  = 'ilu47z5C9YHdvxmKg3N4PNCandBrWJlZwBL4GrnJo'

FACEBOOK_APP_ID                          = '315952661818898'
FACEBOOK_API_SECRET                      = 'e0985397cfd71c44cb1fd1869012fbb3'

SOCIAL_AUTH_COMPLETE_URL_NAME            = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME           = 'socialauth_associate_complete'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL        = "/acc/create/acc3/"
SOCIAL_AUTH_DEFAULT_USERNAME             = 'new_social_auth_user'
SOCIAL_AUTH_UUID_LENGTH                  = 8
SOCIAL_AUTH_EXPIRATION                   = 'expires'
SOCIAL_AUTH_LOGIN_REDIRECT_URL           = '/acc/login/s/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/acc/edit/'
SOCIAL_AUTH_SESSION_EXPIRATION           = False

#
# Crispy forms
#
CRISPY_TEMPLATE_PACK = "bootstrap"
CRISPY_FAIL_SILENTLY = True


#
# ----------------------------------------------------------------------------
# Database settings
# ----------------------------------------------------------------------------
#

DATABASES = {
    'default': {
        'ENGINE'      : 'django.db.backends.postgresql_psycopg2',
        'NAME'        : get_env_variable("DJANGO_DB_NAME"),
        'USER'        : get_env_variable("DJANGO_DB_USER"),
        'PASSWORD'    : get_env_variable("DJANGO_DB_PASSWORD"),
        'HOST'        : get_env_variable("DJANGO_DB_HOST"),
        'PORT'        : '',
        'TEST_NAME'   : get_env_variable("DJANGO_TEST_DB")
    }
}

