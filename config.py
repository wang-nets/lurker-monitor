# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    #Falcon Configure
    FALCON_AGENT = 'http://127.0.0.1:1988/v1/push'

    MONITOR_ITEM = ['cpu', 'disk', 'mem', 'net']
    MONITOR_INTERVAL = 1

    LOG_CFG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(levelname)s: %(message)s '
                          '[in %(pathname)s:%(lineno)d]'
            }
        },
        'handlers': {
            'file': {
                'class': 'logging.handlers.GroupWriteRotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'standard',
                'filename': '/var/log/monitor/monitor.log',
                'maxBytes': 10485760,
                'backupCount': 100,
                'encoding': 'utf8'
            },
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            }
        },
        'loggers': {
            'monitor': {
                'handlers': ['file', 'console'],
                'level': 'INFO'
            }
        }
    }


class DevelopmentConfig(Config):
    REDIS_SERVER = ''


class ProductionConfig(Config):
    pass

CONF = {
    'default':DevelopmentConfig,
    'develop':DevelopmentConfig,
    'production':ProductionConfig
}

global GLOBAL_CONFIG
GLOBAL_CONFIG = CONF['default']

