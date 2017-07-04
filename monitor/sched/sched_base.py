#! -*- coding: UTF-8 -*-
import abc
import logging
from datetime import datetime
from monitor.commons.utils import ModuleLoader
#from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from monitor.sched import singleton
from config import GLOBAL_CONFIG
LOG = logging.getLogger('monitor')


@singleton
class SchedRegistry():

    def __init__(self):
        self._sched = BlockingScheduler()
        monitor_class = map(lambda module: "monitor.sched.sched_collect.%sCollectScheduler" % module.capitalize(),
                            [item for item in GLOBAL_CONFIG.MONITOR_ITEM])
        jobs = ModuleLoader.load_modules(monitor_class)
        for job in jobs:
            self.add_job(job())

    def list_jobs(self):
        return self._sched.get_jobs()

    def add_job(self, sched_job):
        LOG.info("sched_job[%s] add the registry" % sched_job.get_name())
        self._sched.add_job(sched_job.run, trigger=sched_job.get_trigger_type(), **sched_job.get_trigger_args())

    def sched_start(self):
        LOG.debug('The scheduler will be start...')
        self._sched.start()
        LOG.debug('The scheduler started successfully.')

    def sched_stop(self):
        self._sched.shutdown(wait=30)


class AbstractScheduler(object):

    def __init__(self, sched_name=None):
        self._name = sched_name if sched_name is not None else self.__class__.__name__
        self._interval = 1
        self._trigger_type = 'interval'
        self._trigger_unit = 'minutes'
        self._next_run_time = datetime.now()

    def get_name(self):
        return self._name

    def get_func(self):
        return self._func

    def get_interval(self):
        return self._interval

    def get_trigger_type(self):
        return self._trigger_type

    @abc.abstractmethod
    def get_trigger_args(self):
        pass

    @abc.abstractmethod
    def run(self):
        pass
