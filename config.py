# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))
import collections

class Config(object):
    #Rabbitmq
    LIBVIRT = None
    LIBVIRT_TYPE = 'kvm'
    LIBVIRT_URI = ''
    INSTANCES = collections.namedtuple('Instance', ['name', 'UUID', 'state'])
    CPU_STATS = collections.namedtuple('CPUStats', ['number', 'util'])
    INTERFACE = collections.namedtuple('Interface', ['name', 'mac', 'fref', 'parameters'])
    INTERFACE_STATS = collections.namedtuple('InterfaceStats', ['rx_bytes', 'rx_packets', 'tx_bytes', 'tx_packets'])
    DISK = collections.namedtuple('Disk', ['device'])
    DISK_STATS = collections.namedtuple('DiskStats',
                                       ['read_bytes', 'read_requests', 'write_bytes', 'write_requests', 'errors'])
    DISK_SIZE = collections.namedtuple('DiskSize', ['total', 'allocation', 'physical'])


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
                #'class': 'logging.handlers.RotatingFileHandler',
                'class': 'logging.handlers.GroupWriteRotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'standard',
                'filename': '/home/dispatcher/log/dispatcher.log',
                #'filename': 'c://var//log//cloudispatcher//dispatcher.log',
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
            'dispatcher': {
                'handlers': ['file', 'console'],
                'level': 'INFO'
            }
        }
    }
    SALT_ROOT="/srv/salt"

class DevelopmentConfig(Config):


    SQLALCHEMY_DATABASE_URI = "mysql://dispatcher:GomeDevops@DISPATCHER@10.112.2.8:3306/dispatcher?charset=utf8"

    DEBUG = True
    HOST = "0.0.0.0"
    PORT = "8080"
    BACKDOOR_PORT = None

    BROKER_URL = "amqp://admin:Gome@9ijn0okm@10.112.5.24:15600//"
    #CELERY_BROKER_URL = "amqp://guest@10.112.5.24:15600//"
    CELERY_RESULT_BACKEND = "db+sqlite:///./results.sqlite"


class ProductionConfig(Config):
    pass

CONF = {
    'default':DevelopmentConfig,
    'develop':DevelopmentConfig,
    'production':ProductionConfig
}

