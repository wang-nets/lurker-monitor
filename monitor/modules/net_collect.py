import collections
from monitor.modules.collect import Collect
from lxml import etree

INTERFACE = collections.namedtuple('Interface', ['name', 'mac','fref', 'parameters'])
INTERFACE_STATS = collections.namedtuple('InterfaceStats',['rx_bytes', 'rx_packets','tx_bytes', 'tx_packets'])


class NetCollect(Collect):
    def collect_for_down(self, instance_name):
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
            yield INTERFACE(name=name, mac=mac_address,
                            fref=fref, parameters=params)

    def collect(self, instance_name):
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
            interface = INTERFACE(name=name, mac=mac_address,
                                  fref=fref, parameters=params)
            try:
                rx_bytes, rx_packets, _, _, \
                tx_bytes, tx_packets, _, _ = domain.interfaceStats(name)
                stats = INTERFACE_STATS(rx_bytes=rx_bytes,
                                        rx_packets=rx_packets,
                                        tx_bytes=tx_bytes,
                                        tx_packets=tx_packets)
                yield (interface, stats)
            except self.libvirt.libvirtError:
                raise