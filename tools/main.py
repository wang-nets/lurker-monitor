from tools.sched.sched_base import SchedRegistry


class ToolsService(object):
    def __init__(self):
        self.sched = SchedRegistry()

    def start_service(self):
        self.sched.sched_start()


def start_tools():
    service = ToolsService()
    service.start_service()