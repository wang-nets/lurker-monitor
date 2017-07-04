from monitor.modules.collect import Collect

class AliveCollect(Collect):
    def collect(self, instance_name):
        '''
        Collect virtual machine alive infomation.
        1.Get virtual machine status, tell if it's offline or online
        2.Ping virtual machine, tell if it's alive
        '''
        pass