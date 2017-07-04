# -*- coding: utf-8 -*-
from monitor.exceptions import InstanceNotFoundException, InspectorException
import collections
import abc

LIBVIRT = None
LIBVIRT_TYPE = 'kvm'
LIBVIRT_URI = ''
INSTANCE = collections.namedtuple('Instance', ['name', 'UUID', 'state'])


class Collect(object):
    per_type_uris = dict(uml='uml:///system', xen='xen:///', lxc='lxc:///')

    def __init__(self):
        self.uri = self._get_uri()
        self.connection = None
        self.libvirt = __import__('libvirt')

    def _get_uri(self):
        return LIBVIRT_URI or self.per_type_uris.get(LIBVIRT_TYPE,
                                                          'qemu:///system')

    def _get_connection(self):
        if not self.connection or not self._test_connection():
            self.connection = self.libvirt.open(self.uri)
        return self.connection

    def _test_connection(self):
        try:
            self.connection.getCapabilities()
            return True
        except self.libvirt.libvirtError as e:
            if (e.get_error_code() == self.libvirt.VIR_ERR_SYSTEM_ERROR and
                e.get_error_domain() in (self.libvirt.VIR_FROM_REMOTE,
                                         self.libvirt.VIR_FROM_RPC)):
                return False
            raise

    def _lookup_by_name(self, instance_name):
        try:
            return self._get_connection().lookupByName(instance_name)
        except Exception as e:
            if not self.libvirt or not isinstance(e, self.libvirt.libvirtError):
                raise InspectorException(unicode(e))
            error_code = e.get_error_code()
            msg = ("Error from libvirt while looking up %(instance_name)s: "
                   "[Error Code %(error_code)s] "
                   "%(ex)s" % {'instance_name': instance_name,
                               'error_code': error_code,
                               'ex': e})
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
                        yield INSTANCE(name=domain.name(),
                                                    UUID=domain.UUIDString(), state=state)
                except self.libvirt.libvirtError:
                    # Instance was deleted while listing... ignore it
                    pass

    #shut off instances
    def inspect_defined_domains(self):
        if self._get_connection().numOfDomains() > 0:
            for instance_name in self._get_connection().listDefinedDomains():
                domain = self._lookup_by_name(instance_name)
                state = domain.state(0)[0]
                if state != 1:
                    state = 0
                yield INSTANCE(name=instance_name,
                                            UUID=domain.UUIDString(), state=state)

    @abc.abstractmethod
    def collect_for_down(self, instance_name):
        pass

    @abc.abstractmethod
    def collect(self, instance_name):
        pass