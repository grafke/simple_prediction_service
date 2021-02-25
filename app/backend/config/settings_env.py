from envparse import env

PORT = env.int('PORT', default=8123)
DEBUG = env.bool('DEBUG', default=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'

        },
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'loggers': {
        'app': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    },
}

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = ['.mp4']

MAX_CONTENT_LENGTH = 132 * 1024 * 1024

TRAINED_FEATURES = 'resources/rnd_columns.pkl'
TRAINED_MODEL = 'resources/randomfs.pkl'