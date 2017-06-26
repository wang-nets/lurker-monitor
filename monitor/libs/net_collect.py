from monitor.run import MONITOR_CONF
from lxml import etree
from monitor.libs.collect_base import CollectBase

class NetCollect(CollectBase):
    def inspect_vnics_info_for_down(self, instance_name):
        domain = self._lookup_by_name(instance_name)
        tree = etree.fromstring(domain.XMLDesc(0))
        for iface in tree.findall('devices/interface'):
            target = iface.find('target')
            if target is not None:
                name = target.get('dev')
            else:
                continue
            mac = iface.find('mac')
            if mac is not None:
                mac_address = mac.get('address')
            else:
                continue
            fref = iface.find('filterref')
            if fref is not None:
                fref = fref.get('filter')
            params = dict((p.get('name').lower(), p.get('value'))
                          for p in iface.findall('filterref/parameter'))
            yield MONITOR_CONF.INTERFACE(name=name, mac=mac_address,
                            fref=fref, parameters=params)

    def inspect_vnics(self, instance_name):
        domain = self._lookup_by_name(instance_name)
        tree = etree.fromstring(domain.XMLDesc(0))
        for iface in tree.findall('devices/interface'):
            target = iface.find('target')
            if target is not None:
                name = target.get('dev')
            else:
                continue
            mac = iface.find('mac')
            if mac is not None:
                mac_address = mac.get('address')
            else:
                continue
            fref = iface.find('filterref')
            if fref is not None:
                fref = fref.get('filter')
            params = dict((p.get('name').lower(), p.get('value'))
                          for p in iface.findall('filterref/parameter'))
            interface = MONITOR_CONF.INTERFACE(name=name, mac=mac_address,
                                  fref=fref, parameters=params)
            try:
                rx_bytes, rx_packets, _, _, \
                tx_bytes, tx_packets, _, _ = domain.interfaceStats(name)
                stats = MONITOR_CONF.INTERFACE_STATS(rx_bytes=rx_bytes,
                                       rx_packets=rx_packets,
                                       tx_bytes=tx_bytes,
                                       tx_packets=tx_packets)
                yield (interface, stats)
            except libvirt.libvirtError:
                pass