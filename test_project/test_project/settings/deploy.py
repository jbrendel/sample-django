"""
Settings file for deployment run of server.

"""

from .base import *

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CORP_SITE_DOMAIN = SITE_DOMAIN = get_env_variable("DJANGO_SERVER_DNS")
CORP_SITE_SERVER = SITE_SERVER = SITE_DOMAIN + ":" + \
                                            get_env_variable("DJANGO_SERVER_PORT")
CORP_SITE_URL    = SITE_URL    = get_env_variable("DJANGO_SERVER_SCHEMA") + SITE_SERVER

# For Crispy forms
#CRISPY_FAIL_SILENTLY = False

# For general template debugging capabilities
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [ get_env_variable("DJANGO_SERVER_DNS") ]

