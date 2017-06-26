# -*- coding: utf-8 -*-
from lxml import etree
import json
import threading
import time
import abc
import collections
from monitor.run import MONITOR_CONF
from monitor.exceptions.exception import InspectorException, InstanceNotFoundException





class CollectBase():
    per_type_uris = dict(uml='uml:///system', xen='xen:///', lxc='lxc:///')

    def __init__(self):
        self.uri = self._get_uri()
        self.connection = None
        self.libvirt_uri = MONITOR_CONF.get('LIBVIRT_URI')
        self.libvirt_uri = MONITOR_CONF.get('LIBVIRT_TYPE')
        self.instance = collections.namedtuple('Instance', ['name', 'UUID', 'state'])

    def _get_uri(self):
        return self.libvirt_uri or self.per_type_uris.get(self.libvirt_uri,
                                                          'qemu:///system')

    def _get_connection(self):
        if not self.connection or not self._test_connection():
            global libvirt
            if libvirt is None:
                libvirt = __import__('libvirt')
                # LOG.debug('Connecting to libvirt: %s', self.uri)
            self.connection = libvirt.open(self.uri)
        return self.connection

    def _test_connection(self):
        try:
            self.connection.getCapabilities()
            return True
        except libvirt.libvirtError as e:
            if (e.get_error_code() == libvirt.VIR_ERR_SYSTEM_ERROR and
                        e.get_error_domain() in (libvirt.VIR_FROM_REMOTE,
                                                 libvirt.VIR_FROM_RPC)):
                # LOG.debug('Connection to libvirt broke')
                return False
            raise

    def _lookup_by_name(self, instance_name):
        try:
            return self._get_connection().lookupByName(instance_name)
        except Exception as ex:
            if not libvirt or not isinstance(ex, libvirt.libvirtError):
                raise InspectorException(unicode(ex))
            error_code = ex.get_error_code()
            msg = ("Error from libvirt while looking up %(instance_name)s: "
                   "[Error Code %(error_code)s] "
                   "%(ex)s" % {'instance_name': instance_name,
                               'error_code': error_code,
                               'ex': ex})
            raise InstanceNotFoundException(msg)

    def inspect_instances(self):
        if self._get_connection().numOfDomains() > 0:
            for domain_id in self._get_connection().listDomainsID():
                try:
                    # We skip domains with ID 0 (hypervisors).
                    if domain_id != 0:
                        domain = self._get_connection().lookupByID(domain_id)
                        state = domain.state(0)[0]
                        if state != 1:
                            state = 0
                        yield self.instance(name=domain.name(),
                                       UUID=domain.UUIDString(), state=state)
                except libvirt.libvirtError:
                    # Instance was deleted while listing... ignore it
                    pass

    # shut off instances
    def inspect_defined_domains(self):
        if self._get_connection().numOfDomains() > 0:
            for instance_name in self._get_connection().listDefinedDomains():
                domain = self._lookup_by_name(instance_name)
                state = domain.state(0)[0]
                if state != 1:
                    state = 0
                yield self.instance(name=instance_name,
                               UUID=domain.UUIDString(), state=state)

    @abc.abstractmethod
    def collect(self, instance):
        pass

    @abc.abstractmethod
    def collect_for_down(self, instance):
        pass













def output():
    libvirtInspector = LibvirtInspector()
    instances = libvirtInspector.inspect_instances()
    not_running_instances = libvirtInspector.inspect_defined_domains()
    list = []
    for instance in not_running_instances:
        dict = {}
        dict['vmid'] = instance.UUID
        dict['domain_name'] = instance.name
        dict['state'] = instance.state
        cpus = libvirtInspector.inspect_cpus(instance.name)
        dict['cpu'] = cpus.number
        dict['cpu_usage'] = cpus.util
        dict['memory_total'] = libvirtInspector.inspect_mem_info_for_down(instance.name)
        dict['memory_used'] = ""
        dict['memory_usage'] = ""

        # get the nic infomation
        nicList = []
        nicdict = {'nic_name': '', 'mac': '', 'ip': '', 'net_send_read': '', 'net_receive_write': '',
                   'net_send_request': '', 'net_receive_reques': ''}
        nicList.append(nicdict)
        dict['nics'] = nicList
        # get the disk infomation
        disks = libvirtInspector.inspect_disk_info_for_down(instance.name)
        diskList = []
        for disk in disks:
            diskdict = {}
            diskdict['device'] = disk[0].device
            diskdict['total_size'] = disk[1].total
            diskdict['used_size'] = disk[1].physical
            diskdict['disk_read'] = ""
            diskdict['disk_write'] = ""
            diskdict['disk_read_request'] = ""
            diskdict['disk_write_request'] = ""
            diskList.append(diskdict)
        dict['disks'] = diskList
        list.append(dict)
    for instance in instances:
        memory = libvirtInspector.inspect_memory(instance.name)
        dict = {}
        dict['vmid'] = instance.UUID
        dict['domain_name'] = instance.name
        dict['state'] = instance.state
        cpus = libvirtInspector.inspect_cpus(instance.name)
        dict['cpu'] = cpus.number
        dict['cpu_usage'] = cpus.util
        dict['memory_total'] = memory.total
        dict['memory_used'] = memory.used
        dict['memory_usage'] = memory.util
        # get the nic infomation
        nics = libvirtInspector.inspect_vnics(instance.name)
        nicList = []
        for nic in nics:
            nicdict = {}
            nicdict['nic_name'] = nic[0].name
            nicdict['mac'] = nic[0].mac
            nicdict['ip'] = nic[0].parameters.get('ip', '')
            nicdict['net_send_read'] = nic[1].tx_bytes
            nicdict['net_receive_write'] = nic[1].rx_bytes
            nicdict['net_send_request'] = nic[1].tx_packets
            nicdict['net_receive_reques'] = nic[1].rx_packets
            nicList.append(nicdict)
        dict['nics'] = nicList
        # get the disk infomation
        disks = libvirtInspector.inspect_disks(instance.name)
        diskList = []
        for disk in disks:
            diskdict = {}
            diskdict['device'] = disk[0].device
            diskdict['total_size'] = disk[2].total
            diskdict['used_size'] = disk[2].physical
            diskdict['disk_read'] = disk[1].read_bytes
            diskdict['disk_write'] = disk[1].write_bytes
            diskdict['disk_read_request'] = disk[1].read_requests
            diskdict['disk_write_request'] = disk[1].write_requests
            diskList.append(diskdict)
        dict['disks'] = diskList
        list.append(dict)


def main():
    output()


if __name__ == "__main__":
    main()

