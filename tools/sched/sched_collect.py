from tools.modules.redis_collect import RedisCollect
from threading import Thread
import traceback
from config import GLOBAL_CONFIG
import logging
from tools.sched.sched_base import AbstractScheduler
from tools.falcon.falcon_api import FalconApi
LOG = logging.getLogger('monitor')


class RedisCollectService(Thread):
    def do_collect(self):
        redis = RedisCollect()
        host_list = redis.traverse_redis()
        falcon = FalconApi()
        falcon.add_host_to_hostgroup(host_list=host_list, hostgroup_id=GLOBAL_CONFIG.FALCON_HOST_GROUP_ID)


class RedisCollectScheduler(AbstractScheduler):
    def __init__(self):
        super(RedisCollectScheduler, self).__init__()
        self._interval = 1

    def run(self):
        RedisCollectService().do_collect()

    def get_trigger_args(self):
        return {self._trigger_unit: self._interval, 'next_run_time': self._next_run_time}