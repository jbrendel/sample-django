"""
Settings file for local development run of server.

- Enables debugging
- Installs Django-debug-toolbar

"""

from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CORP_SITE_DOMAIN = SITE_DOMAIN = "localhost"
CORP_SITE_SERVER = SITE_SERVER = SITE_DOMAIN+":8000"
CORP_SITE_URL    = SITE_URL    = "http://" + SITE_SERVER

#
# Some DEBUG related settings
#

'''
# For the Django debug toolbar
MIDDLEWARE_CLASSES  += ( 'debug_toolbar.middleware.DebugToolbarMiddleware', )
INTERNAL_IPS         = ('127.0.0.1',)
INSTALLED_APPS      += ( 'debug_toolbar', )
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}
'''

# For Crispy forms
#CRISPY_FAIL_SILENTLY = False

# For general template debugging capabilities
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

