#! -*- coding: UTF-8 -*-
import abc
from datetime import datetime
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from monitor.run import MONITOR_CONF
from monitor.sched import singleton
LOG = logging.getLogger('lurker_monitor')


@singleton
class SchedRegistry(object):

    def __init__(self):
        self._jobstores = CONF.SCHED.jobstores
        self._executors = CONF.SCHED.executors
        self._sched = BackgroundScheduler()
        jobs = ModuleLoader.load_modules(CONF.SCHED.job_classes)
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
        self._sched.shutdown(wait=CONF.SCHED.shutdown_wait)


class AbstractScheduler(object):

    def __init__(self, sched_name=None):
        self._name = sched_name if sched_name is not None else self.__class__.__name__
        self._interval = 1
        self._trigger_type = CONF.SCHED.trigger_type
        self._trigger_unit = CONF.SCHED.trigger_unit
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
