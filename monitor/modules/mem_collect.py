from monitor.modules.collect import Collect
import collections

MEMORY = collections.namedtuple('Memory',['total','used','util'])


class MemCollect(Collect):
    def collect_for_down(self, instance_name):
        domain = self._lookup_by_name(instance_name)
        mem_total = domain.info()[1]
        return mem_total

    def collect(self, instance_name):
        try:
            domain = self._lookup_by_name(instance_name)
            domain.setMemoryStatsPeriod(5)
            free_mem = float(domain.memoryStats()['unused'])
            total_mem = float(domain.memoryStats()['available'])
            util = (float(total_mem - free_mem) / float(total_mem)) * 100
            return MEMORY(total=total_mem, used=total_mem - free_mem, util=util)
        except:
            try:
                domain = self._lookup_by_name(instance_name)
                actual = float(domain.memoryStats()['actual'])
                rss = float(domain.memoryStats()['rss'])
                rss = rss - 150000
                if rss >= actual:
                    rss = rss - 250000
                if rss <= 0:
                    rss = rss + 150000
                util = (rss / actual) * 100
                return MEMORY(total=actual, used=rss, util=util)
            except self.libvirt.libvirtError:
                raise