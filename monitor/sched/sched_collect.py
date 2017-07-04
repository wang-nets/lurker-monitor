#! -*- coding:UTF-8 -*-
from monitor.sched.sched_base import AbstractScheduler
from monitor.modules.cpu_collect import CpuCollect
from monitor.modules.disk_collect import DiskCollect
from monitor.modules.mem_collect import MemCollect
from monitor.modules.net_collect import NetCollect
from monitor.falcon.falcon import Falcon
from threading import Thread
import traceback
import logging
LOG = logging.getLogger('monitor')


class NetCollectService(Thread):

    def do_collect(self):
        LOG.info("===============Start collect network interface================")
        try:
            collect = NetCollect()
            falcon = Falcon()
            for instance in collect.inspect_instances():
                vnics = collect.collect(instance.name)
                endpoint = instance.name
                for nic in vnics:
                    falcon.push(endpoint, 'net.if.out.bytes', 60,
                                nic[1].tx_bytes, 'COUNTER', 'iface=%s' % nic[0].name)
                    falcon.push(endpoint, 'net.if.in.bytes', 60,
                                nic[1].rx_bytes, 'COUNTER', 'iface=%s' % nic[0].name)
                    falcon.push(endpoint, 'net.if.out.packets', 60,
                                nic[1].tx_packets, 'COUNTER', 'iface=%s' % nic[0].name)
                    falcon.push(endpoint, 'net.if.in.packets', 60,
                                nic[1].rx_packets, 'COUNTER', 'iface=%s' % nic[0].name)
        except Exception as e:
            LOG.error('Collect network info failed: %s' % traceback.format_exc())


class CpuCollectService(Thread):

    def do_collect(self):
        LOG.info("===============Start collect cpu ================")
        try:
            collect = CpuCollect()
            falcon = Falcon()
            for instance in collect.inspect_instances():
                vcpus = collect.collect(instance.name)
                endpoint = instance.name
                cpu_idle = 100 - float(vcpus.util)
                falcon.push(endpoint, 'cpu.idle', 60,
                            cpu_idle, 'GAUGE')

        except Exception as e:
            LOG.error('Collect cpu info failed: %s' % traceback.format_exc())



class DiskCollectService(Thread):

    def do_collect(self):
        LOG.info("===============Start collect disk================")
        try:
            collect = DiskCollect()
            falcon = Falcon()
            for instance in collect.inspect_instances():
                disks = collect.collect(instance.name)
                endpoint = instance.name
                for disk in disks:
                    #df.bytes.free.percent/fstype=ext4,mount=/boot
                    if disk[2].total == 0:
                        used_percent = 0
                    else:
                        used_percent = disk[2].physical / disk[2].total
                    falcon.push(endpoint, 'disk.bytes.free.percent', 60,
                                used_percent, 'GAUGE', 'dev=%s' % disk[0].device)
                    #disk.io.read_requests/device=sda
                    falcon.push(endpoint, 'disk.io.read_requests', 60,
                                disk[1].read_requests, 'COUNTER', 'dev=%s' % disk[0].device)
                    falcon.push(endpoint, 'disk.io.write_requests', 60,
                                disk[1].write_requests, 'COUNTER', 'dev=%s' % disk[0].device)
        except Exception as e:
            LOG.error('Collect disk info failed: %s' % traceback.format_exc())


class MemCollectService(Thread):

    def do_collect(self):
        LOG.info("===============Start collect mem================")
        try:
            collect = MemCollect()
            falcon = Falcon
            for instance in collect.inspect_instances():
                mems = collect.collect(instance.name)
                endpoint = instance.name
                if mems.total == 0:
                    memory_idle = 0
                else:
                    memory_idle = (mems.total - mems.used) / mems.total
                falcon.push(endpoint, 'mem.memfree.percent', 60,
                            memory_idle, 'GAUGE')

        except Exception as e:
            LOG.error("Collect memory info failed: %s" % traceback.format_exc())


class NetCollectScheduler(AbstractScheduler):

    def __init__(self):
        super(NetCollectScheduler, self).__init__()
        self._interval = 1

    def run(self):
        NetCollectService().do_collect()

    def get_trigger_args(self):
        return {self._trigger_unit: self._interval, 'next_run_time': self._next_run_time}


class CpuCollectScheduler(AbstractScheduler):

    def __init__(self):
        super(CpuCollectScheduler, self).__init__()
        self._interval = 1

    def run(self):
        CpuCollectService().do_collect()

    def get_trigger_args(self):
        return {self._trigger_unit: self._interval, 'next_run_time': self._next_run_time}


class DiskCollectScheduler(AbstractScheduler):

    def __init__(self):
        super(DiskCollectScheduler, self).__init__()
        self._interval = 1

    def run(self):
        DiskCollectService().do_collect()

    def get_trigger_args(self):
        return {self._trigger_unit: self._interval, 'next_run_time': self._next_run_time}


class MemCollectScheduler(AbstractScheduler):

    def __init__(self):
        super(MemCollectScheduler, self).__init__()
        self._interval = 1

    def run(self):
        MemCollectService().do_collect()

    def get_trigger_args(self):
        return {self._trigger_unit: self._interval, 'next_run_time': self._next_run_time}

