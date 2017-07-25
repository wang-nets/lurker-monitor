from tools.sched.sched_base import SchedRegistry


class RedisService(object):
    def __init__(self):
        self.sched = SchedRegistry()

    def start_service(self):
        self.sched.sched_start()


def start_redis():
    service = RedisService()
    service.start_service()