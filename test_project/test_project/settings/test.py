"""
Settings file for unit tests.

"""

import datetime

from .local import *

#
# Disable logging during test runs
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
    },
}

#
# Email backend for testing
#
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

#
# Coverage related testing setup
#

now = str(datetime.datetime.now())
TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'

"""
# Enable this one if you want to have time-stamped, per-user coverage reports.
# Otherwise, just leave it at the simpler static setting below...
import getpass
COVERAGE_REPORT_HTML_OUTPUT_DIR = '/var/www/%s/coverage/zzyyxx/%s' % \
                                                            (getpass.getuser(), now)
"""
COVERAGE_REPORT_HTML_OUTPUT_DIR = get_env_variable("COVERAGE_LOCATION",
                                            default='/var/www/coverage/zzyyxx/')

