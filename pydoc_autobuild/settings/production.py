# In production set the environment variable like this:
#    DJANGO_SETTINGS_MODULE=my_proj.settings.production
from .base import *             # NOQA
import logging.config

# For security and performance reasons, DEBUG is turned off
DEBUG = False

# Must mention ALLOWED_HOSTS in production!
ALLOWED_HOSTS = ['docs.python.org.tw']


# Cache the templates in memory for speed-up
loaders = [
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
    ),
]

TEMPLATES[0]['OPTIONS'].update({"loaders": loaders})
TEMPLATES[0]['OPTIONS'].update({"debug": False})
del TEMPLATES[0]['APP_DIRS']

# Explicitly tell Django where to find translations.
LOCALE_PATHS = [join(BASE_DIR, 'locale')]

# Increase Django-Q number of saved results
Q_CLUSTER['save_limit'] = 25
# Decrease number of tasks in memory
Q_CLUSTER['queue_limit'] = 5
# Increase default timeout time
Q_CLUSTER['timeout'] = 3600

# Log everything to the logs directory at the top
LOGFILE_ROOT = join(BASE_DIR, 'logs')

# Reset logging
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
        'proj_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(LOGFILE_ROOT, 'project.log'),
            'formatter': 'verbose'
        },
        'django_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': join(LOGFILE_ROOT, 'django.log'),
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
            'handlers': ['django_log_file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'project': {
            'handlers': ['proj_log_file'],
            'level': 'DEBUG',
        },
    }
}

logging.config.dictConfig(LOGGING)
