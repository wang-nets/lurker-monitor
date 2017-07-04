#! -*- coding:UTF-8 -*-
from monitor.sched.sched_base import AbstractScheduler
from monitor.modules.cpu_collect import CpuCollect
from monitor.modules.disk_collect import DiskCollect
from monitor.modules.mem_collect import MemCollect
from monitor.modules.net_collect import NetCollect
from monitor.falcon.falcon import Falcon
from threading import Thread
import logging
LOG = logging.getLogger('monitor')


class NetCollectService(Thread):

    def do_collect(self):
        LOG.info("===============Start collect network interface================")
        net = NetCollect()
        falcon = Falcon()
        for instance in net.inspect_instances():
            vnics = net.collect(instance.name)
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


class CpuCollectService(Thread):

    def do_collect(self):
        LOG.info("===============Start collect cpu ================")
        cpu = CpuCollect()
        falcon = Falcon()
        for instance in cpu.inspect_instances():
            vcpus = cpu.collect(instance.name)
            endpoint = instance.name
            cpus = vcpus.inspect_cpus(instance.name)
            cpu_idle = 100 - float(cpus.util)
            falcon.push(endpoint, 'cpu.idle', 60,
                        cpu_idle, 'GAUGE')



class DiskCollectService(Thread):

    def do_collect(self):
        LOG.info("===============Start collect disk================")
        disk = DiskCollect()
        falcon = Falcon()
        for instance in disk.inspect_instances():
            disks = disk.collect(instance.name)
            endpoint = instance.name
            for disk in disks:
                #df.bytes.free.percent/fstype=ext4,mount=/boot
                used_percent = disk[2].physical / disk[2].total
                falcon.push(endpoint, 'disk.bytes.free.percent', 60,
                            used_percent, 'GAUGE', 'dev=%s' % disk[0].device)
                #disk.io.read_requests/device=sda
                falcon.push(endpoint, 'disk.io.read_requests', 60,
                            disk[1].read_requests, 'COUNTER', 'dev=%s' % disk[0].device)
                falcon.push(endpoint, 'disk.io.write_requests', 60,
                            disk[1].write_requests, 'COUNTER', 'dev=%s' % disk[0].device)


class MemCollectService(Thread):

    def do_collect(self):
        LOG.info("===============Start collect mem================")
        mem = MemCollect()
        falcon = Falcon
        for instance in mem.inspect_instances():
            mems = mem.collect(instance.name)
            endpoint = instance.name
            memory_idle = (mems.total - mems.used) / mems.total
            falcon.push(endpoint, 'mem.memfree.percent', 60,
                        memory_idle, 'GAUGE')



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

