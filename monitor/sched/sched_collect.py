#! -*- coding:UTF-8 -*-
from monitor.sched.sched_base import AbstractScheduler
from monitor.modules.cpu_collect import CpuCollect
from monitor.modules.disk_collect import DiskCollect
from monitor.modules.mem_collect import MemCollect
from monitor.modules.net_collect import NetCollect
from monitor.falcon.falcon import Falcon
import datetime
from threading import Thread


class NetCollectService(Thread):
    def do_transact(self):
        net = NetCollect()
        for instance in net.inspect_instances():
            vnics = net.collect(instance.name)
            for nic in vnics:



class CpuCollectService(Thread):
    def do_transact(self):
        pass


class DiskCollectService(Thread):
    def do_transact(self):
        pass


class MemCollectService(Thread):
    def do_transact(self):
        pass

class NetCollectScheduler(AbstractScheduler):

    def __init__(self):
        super(NetCollectScheduler, self).__init__()
        self._interval = 1

    def run(self):
        NetCollectService().do_transact()

    def get_trigger_args(self):
        return {self._trigger_unit: self._interval, 'next_run_time': self._next_run_time}


class CpuCollectSchduler(AbstractScheduler):

    def __init__(self):
        super(CpuCollectSchduler, self).__init__()
        self._interval = 1

    def run(self):
        CpuCollectService().do_transact()

    def get_trigger_args(self):
        return {self._trigger_unit: self._interval, 'next_run_time': self._next_run_time}

class DiskCollectSchduler(AbstractScheduler):

    def __init__(self):
        super(DiskCollectSchduler, self).__init__()
        self._interval = 1

    def run(self):
        DiskCollectService().do_transact()

    def get_trigger_args(self):
        return {self._trigger_unit: self._interval, 'next_run_time': self._next_run_time}


class MemCollectSchduler(AbstractScheduler):

    def __init__(self):
        super(MemCollectSchduler, self).__init__()
        self._interval = 1

    def run(self):
        MemCollectService().do_transact()

    def get_trigger_args(self):
        return {self._trigger_unit: self._interval, 'next_run_time': self._next_run_time}

