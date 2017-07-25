# -*- coding: utf-8 -*-
from config import CONF
import logging
import logging.config
import multiprocessing
from monitor.main import start_monitor
from tools.main import start_redis
from config import GLOBAL_CONFIG
LOG = logging.getLogger("monitor")


def create_app():

    from logging import Formatter, handlers
    from logging.handlers import RotatingFileHandler
    from logging import StreamHandler
    from logging.config import dictConfig
    from logging import DEBUG
    import os
    import stat
    import sys


    class GroupWriteRotatingFileHandler(handlers.RotatingFileHandler):
        def doRollover(self):
            """
            Override base class method to make the new log file group writable.
            """
            # Rotate the file first.
            handlers.RotatingFileHandler.doRollover(self)

            # Add group write to the current permissions.
            try:
                currMode = os.stat(self.baseFilename).st_mode
                os.chmod(self.baseFilename, currMode | stat.S_IWGRP)
            except OSError:
                pass

    handlers.GroupWriteRotatingFileHandler = GroupWriteRotatingFileHandler

    def setup_logging():
        """
        Logging in security_monkey can be configured in two ways.

        1) Vintage: Set LOG_FILE and LOG_LEVEL in your config.
        LOG_FILE will default to stderr if no value is supplied.
        LOG_LEVEL will default to DEBUG if no value is supplied.

            LOG_LEVEL = "DEBUG"
            LOG_FILE = "/var/log/security_monkey/securitymonkey.log"

        2) Set LOG_CFG in your config to a PEP-0391 compatible
        logging configuration.

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
                        'class': 'logging.handlers.RotatingFileHandler',
                        'level': 'DEBUG',
                        'formatter': 'standard',
                        'filename': '/var/log/security_monkey/securitymonkey.log',
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
                    'security_monkey': {
                        'handlers': ['file', 'console'],
                        'level': 'DEBUG'
                    },
                    'apscheduler': {
                        'handlers': ['file', 'console'],
                        'level': 'INFO'
                    }
                }
            }
        """

        if GLOBAL_CONFIG.DEBUG:
            if GLOBAL_CONFIG.LOG_CFG:
                # initialize the Flask logger (removes all handlers)
                logging.config.dictConfig(GLOBAL_CONFIG.LOG_CFG)
            else:
                # capability with previous config settings
                # Should have LOG_FILE and LOG_LEVEL set
                if GLOBAL_CONFIG.LOG_FILE is not None:
                    handler = RotatingFileHandler(GLOBAL_CONFIG.LOG_FILE, maxBytes=10000000, backupCount=100)
                else:
                    handler = StreamHandler(stream=sys.stderr)

                handler.setFormatter(
                    Formatter('%(asctime)s %(levelname)s: %(message)s '
                              '[in %(pathname)s:%(lineno)d]')
                )
                logging.getLogger(__name__).setLevel(GLOBAL_CONFIG.LOG_LEVEL)
                logging.getLogger(__name__).addHandler()

    setup_logging()
    service_list = list()
    if 'monitor' in GLOBAL_CONFIG.METHOD:
        service = multiprocessing.Process(target=start_monitor)
        service_list.append(service)
    if 'redis' in GLOBAL_CONFIG.METHOD:
        service = multiprocessing.Process(target=start_redis)
        service_list.append(service)

    for service in service_list:
        service.start()



if __name__ == '__main__':
    create_app()