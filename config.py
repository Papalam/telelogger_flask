import logging


LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': "[%(asctime)s] [%(levelname)s] - %(name)s: %(message)s",
            'datefmt': '%d-%m-%Y %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': 'telebot_flask.log',
        },
    },
    'loggers': {
        'telebot_flask': {
            'handlers': ['file', ],
            'level': logging.DEBUG
        },
    },
}
