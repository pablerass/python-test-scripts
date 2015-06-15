#!/usr/bin/env python3

import logging, logging.config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)-7s - %(name)s - %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)-7s: %(name)s - %(message)s',
        },
    },
    'handlers': {
        'file_last':{
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': 'file_last.log',
            'mode': 'w',
            'encoding': 'utf-8',
        },
        'file_perm':{
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': 'file_perm.log',
            'mode': 'a',
            'encoding': 'utf-8',
            'maxBytes': 2560,
            'backupCount': 10,
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file_perm', 'file_last', 'console'],
    },
}

def main():
    logging.config.dictConfig(LOGGING)
    logger_main = logging.getLogger('main')
    logger_other = logging.getLogger('other')
    logging.debug('Debug')
    logger_main.info('Info')
    logger_other.warning('Warning')
    logging.error('Error')

if __name__ == '__main__':
    main()