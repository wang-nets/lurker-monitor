import redis
from config import GLOBAL_CONFIG
import json


class RedisCollect(object):
    def __init__(self):
        pool = redis.ConnectionPool(host=GLOBAL_CONFIG.REDIS_SERVER, port=GLOBAL_CONFIG.REDIS_PORT,
                                    db=GLOBAL_CONFIG.REDIS_DB, password=GLOBAL_CONFIG.REDIS_PASSWD)
        self.r = redis.StrictRedis(connection_pool=pool)

    def traverse_redis(self):
        try:
            host_list = list()
            for key in self.r.scan_iter(match='kvm-id-*'):
                json_data = self.r.get(key)
                host_attr = json.loads(json_data)
                if 'hostname' not in host_attr:
                    raise ValueError
                host_list.append(host_attr['hostname'])

            return host_list
        except ValueError:
            pass
        except Exception as e:
            pass
