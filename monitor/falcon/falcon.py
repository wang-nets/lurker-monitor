import requests
import json
from config import GLOBAL_CONFIG
from monitor.exceptions import HttpRequestException
import time
import logging
import traceback

LOG = logging.getLogger("monitor")


class Falcon(object):
    def push(self, endpoint, metric, step, value, coutertype, tags = None):
        try:
            falcon_agent = GLOBAL_CONFIG.FALCON_AGENT
            payload = self._format_data(endpoint, metric, step, value, coutertype, tags)
            print payload
            req = requests.post(falcon_agent, data=json.dumps(payload))
            if req.status_code != 200:
                raise HttpRequestException
        except HttpRequestException:
            LOG.error("Http request failed:%s, status code:%d" %
                      (req.text, req.status_code))
            print traceback.format_exc()
        except Exception as e:
            print traceback.format_exc()
            raise

    def _format_data(self, endpoint, metric, step, value, coutertype, tags):
        data_list = list()
        data_dict = dict()
        data_dict['endpoint'] = endpoint
        data_dict['metric'] = metric
        data_dict['timestamp'] = int(time.time())
        data_dict['step'] = step
        data_dict['value'] = value
        data_dict['counterType'] = coutertype
        if tags:
            data_dict['tags'] = tags
        data_list.append(data_dict)
        return data_list

