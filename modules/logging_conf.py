import os
from logging.config import dictConfig


def configure_logging(filename: str = "app", level: str = 'DEBUG') -> None:
    log_path = os.path.join('logs', '{}.log'.format(filename))
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    dictConfig({
        'version': 1,
        "disable_existing_loggers": False,
        'formatters': {
            'console': {
                'class': 'logging.Formatter',
                'datefmt': '%Y-%m-%d %H:%M:%S',
                'format': '%(asctime)s %(levelname)-8s | %(name)-20s:%(lineno)-3s | %(message)s',
            },
            'file': {
                'class': 'logging.Formatter',
                'datefmt': '%Y-%m-%d %H:%M:%S',
                'format': '%(asctime)s %(levelname)-8s | %(name)-20s:%(lineno)-3s | %(message)s',
            }
        },
        'handlers': {
            'default': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'console',
            },
            'rotating_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': log_path,
                'maxBytes': 1024 * 1024,
                'backupCount': 3,
                'level': 'INFO',
                'formatter': 'file',
                "encoding": "utf8",
            },
        },
        "loggers": {
            '__main__': {
                'level': level,
                'handlers': ['default', 'rotating_file'],
            },
            'modules': {
                'level': level,
                'handlers': ['default', 'rotating_file'],
                'propagate': True,
            },
        }
    })
