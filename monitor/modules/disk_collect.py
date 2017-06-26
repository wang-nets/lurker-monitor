import collections
from monitor.modules.collect import Collect
from lxml import etree

DISK = collections.namedtuple('Disk', ['device'])
DISK_STATS = collections.namedtuple('DiskStats',['read_bytes', 'read_requests','write_bytes', 'write_requests','errors'])
DISK_SIZE = collections.namedtuple('DiskSize',['total','allocation','physical'])

class DiskCollect(Collect):
    def collect_for_down(self, instance_name):
        domain = self._lookup_by_name(instance_name)
        tree = etree.fromstring(domain.XMLDesc(0))
        for device in filter(
                bool,
                [target.get("dev")
                 for target in tree.findall('devices/disk/target')]):
            disk = DISK(device=device)
            try:
                disk_size = domain.blockInfo(device,0)
            except self.libvirt.libvirtError:
                disk_size = [0,0,0]
                pass
            size = DISK_SIZE(total=disk_size[0]/(1024*1024),allocation=disk_size[1]/(1024*1024),physical=disk_size[2]/(1024*1024))
            yield (disk,size)

    def collect(self, instance_name):
        domain = self._lookup_by_name(instance_name)
        tree = etree.fromstring(domain.XMLDesc(0))
        for device in filter(
                bool,
                [target.get("dev")
                 for target in tree.findall('devices/disk/target')]):
            disk = DISK(device=device)
            block_stats = domain.blockStats(device)
            stats = DISK_STATS(read_requests=block_stats[0],
                              read_bytes=block_stats[1],
                              write_requests=block_stats[2],
                              write_bytes=block_stats[3],
                              errors=block_stats[4])
            try:
                disk_size = domain.blockInfo(device, 0)
            except self.libvirt.libvirtError:
                disk_size = [0, 0, 0]

            finally:
                size = DISK_SIZE(total=disk_size[0] / (1024 * 1024), allocation=disk_size[1] / (1024 * 1024),
                                 physical=disk_size[2] / (1024 * 1024))
                yield (disk, stats, size)