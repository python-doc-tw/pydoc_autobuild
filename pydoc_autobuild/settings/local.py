from .base import *             # noqa
import sys
import logging.config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
WERKZEUG_DEBUG = True

# Django Debug Toolbar
INSTALLED_APPS += ('debug_toolbar.apps.DebugToolbarConfig',)


# Log everything to the logs directory at the top
LOGFILE_ROOT = join(BASE_DIR, 'logs')

# Reset logging
# http://www.caktusgroup.com/blog/2015/01/27/
# Django-Logging-Configuration-logging_config-default-settings-logger/

LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': (
                '[%(asctime)s] %(levelname)s '
                '[%(pathname)s:%(lineno)s] %(message)s'
            ),
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'django_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(LOGFILE_ROOT, 'django.log'),
            'formatter': 'verbose'
        },
        'proj_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(LOGFILE_ROOT, 'project.log'),
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['django_log_file', ],
            'propagate': True,
            'level': 'DEBUG',
        },
        # 'project': {
        #     'handlers': ['proj_log_file', 'console', ],
        #     'level': 'DEBUG',
        # },
    }
}

for app in LOCAL_APPS:
    LOGGING['loggers'][app] = {
        'handlers': ['proj_log_file', 'console', ],
        'level': 'DEBUG',
    }

logging.config.dictConfig(LOGGING)

