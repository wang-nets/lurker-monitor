# -*- coding: utf-8 -*-
from monitor.modules.collect import Collect
import collections

CPU_STATS = collections.namedtuple('CPUStats', ['number', 'util'])


class CpuCollect(Collect):
    def collect(self, instance_name):
        domain = self._lookup_by_name(instance_name)
        try:
            (_, _, _, num_cpu, cpu_time_start) = domain.info()
            import time
            real_time_start = time.time()
            time.sleep(1)
            (_, _, _, _, cpu_time_end) = domain.info()
            real_time_end = time.time()
            real_diff_time = real_time_end - real_time_start
            util = 100 * (cpu_time_end - cpu_time_start) / (float)(num_cpu * real_diff_time * 1000000000)
            if util > 100:
                util = 100.0
            if util < 0:
                util = 0.0
            return CPU_STATS(number=num_cpu, util=str(util))
        except self.libvirt.libvirtError:
            pass
