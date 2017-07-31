import json
import logging
import time

import requests
from redis import Redis

from cfg import GLOBAL_CONFIG
from monitor.exceptions import HttpRequestException,RedisNotFoundException

LOG = logging.getLogger("monitor")


class Falcon(object):
    def __init__(self):
        self.redis_client = Redis(host=GLOBAL_CONFIG.REDIS_SERVER,
                                  port=GLOBAL_CONFIG.REDIS_PORT, db=GLOBAL_CONFIG.REDIS_DB,
                                  password=GLOBAL_CONFIG.REDIS_PASSWD)

    def push(self, endpoint, metric, step, value, countertype, tags = None):
        '''
        push data to falcon agent
        '''
        try:
            falcon_agent = GLOBAL_CONFIG.FALCON_AGENT
            json_info = self.redis_client.get(endpoint)
            if not json_info:
                raise RedisNotFoundException('Cannot find host info in redis[%s]' % endpoint)
            else:
                hostinfo = json.loads(json_info)
                hostname = hostinfo['hostname']
            payload = self._format_data(hostname, metric, step, value, countertype, tags)
            req = requests.post(falcon_agent, data=json.dumps(payload))
            if req.status_code != 200:
                raise HttpRequestException
        except HttpRequestException:
            LOG.error("Http request failed:%s, status code:%d" %
                      (req.text, req.status_code))
        except Exception as e:
            pass

    def batch_push(self, data_list):
        pass

    @staticmethod
    def __formart_data_list(data_list):
        pass

    @staticmethod
    def _format_data(endpoint, metric, step, value, countertype, tags):
        '''

        :param endpoint: hostname
        :param metric: monitor item cpu.idle ..
        :param step: interval, the default is 60s
        :param value: value
        :param countertype: the type of item, GAUGE or COUNTER
        :param tags: item tag
        :return:
        The format of falcon data must be list
        '''
        data_list = list()
        data_dict = dict()
        data_dict['endpoint'] = endpoint
        data_dict['metric'] = metric
        data_dict['timestamp'] = int(time.time())
        data_dict['step'] = step
        data_dict['value'] = value
        data_dict['counterType'] = countertype
        if tags:
            data_dict['tags'] = tags
        data_list.append(data_dict)
        return data_list

