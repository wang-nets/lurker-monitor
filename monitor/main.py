from monitor.sched.sched_base import SchedRegistry


class MonitorService(object):
    def __init__(self):
        self.sched = SchedRegistry()

    def start_service(self):
        self.sched.sched_start()


def start_monitor():
    service = MonitorService()
    service.start_service()