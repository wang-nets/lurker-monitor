from monitor.run import MONITOR_CONF
from monitor.libs.collect_base import CollectBase
import collections

class MemCollect(CollectBase):
    def __init__(self):
        self.memory = collections.namedtuple('Memory', ['total', 'used', 'util'])

    def collect_for_down(self, instance_name):
        domain = self._lookup_by_name(instance_name)
        mem_total = domain.info()[1]
        return mem_total

    def collect(self, instance_name):
        try:
            domain = self._lookup_by_name(instance_name)
            domain.setMemoryStatsPeriod(5)
            meminfo = domain.memoryStats()
            free_mem = float(meminfo['unused'])
            total_mem = float(meminfo['available'])
            util = ((total_mem - free_mem) / total_mem) * 100
            return MONITOR_CONF.MEMORY(total=total_mem, used=total_mem - free_mem, util=util)
        except:
            pass
        try:
            domain = self._lookup_by_name(instance_name)
            actual = float(domain.memoryStats()['actual'])
            rss = float(domain.memoryStats()['rss'])
            rss = rss - 150000
            if rss >= actual:
                rss = rss - 250000
            if rss <= 0:
                rss = rss + 150000
            # util = str(int((rss / actual)*100))
            util = (rss / actual) * 100
            # import decimal
            # util = decimal.Decimal(str(round(util, 0)))
            return self.memory(total=actual, used=rss, util=util)
        except libvirt.libvirtError:
            pass