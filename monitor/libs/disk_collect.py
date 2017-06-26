from monitor.run import MONITOR_CONF
from lxml import etree
from monitor.libs.collect_base import CollectBase


class DiskCollect(CollectBase):
    def inspect_disk_info_for_down(self, instance_name):
        domain = self._lookup_by_name(instance_name)
        # mem_total = domain.info()[1]
        tree = etree.fromstring(domain.XMLDesc(0))
        for device in filter(
                bool,
                [target.get("dev")
                 for target in tree.findall('devices/disk/target')]):
            disk = MONITOR_CONF.DISK(device=device)
            try:
                disk_size = domain.blockInfo(device, 0)
            except libvirt.libvirtError:
                disk_size = [0, 0, 0]
                pass
            size = MONITOR_CONF.DISK_SIZE(total=disk_size[0] / (1024 * 1024), allocation=disk_size[1] / (1024 * 1024),
                            physical=disk_size[2] / (1024 * 1024))
            yield (disk, size)

    def inspect_disks(self, instance_name):
        domain = self._lookup_by_name(instance_name)
        tree = etree.fromstring(domain.XMLDesc(0))
        for device in filter(
                bool,
                [target.get("dev")
                 for target in tree.findall('devices/disk/target')]):
            disk = MONITOR_CONF.DISK(device=device)
            block_stats = domain.blockStats(device)
            stats = MONITOR_CONF.DISK_STATS(read_requests=block_stats[0],
                              read_bytes=block_stats[1],
                              write_requests=block_stats[2],
                              write_bytes=block_stats[3],
                              errors=block_stats[4])
            try:
                disk_size = domain.blockInfo(device, 0)
            except libvirt.libvirtError:
                disk_size = [0, 0, 0]
                pass
            size = MONITOR_CONF.DISK_SIZE(total=disk_size[0] / (1024 * 1024), allocation=disk_size[1] / (1024 * 1024),
                            physical=disk_size[2] / (1024 * 1024))
            yield (disk, stats, size)