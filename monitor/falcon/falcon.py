import requests
import json
from app import MONITOR_CONF
from monitor.exceptions import HttpRequestException
import logging

LOG = logging.getLogger("monitor")


class Falcon(object):
    def push(self, payload):
        try:
            falcon_agent = MONITOR_CONF.FALCON_AGENT
            req = requests.post(falcon_agent, data=json.dumps(payload))
            if req.status_code != 200:
                raise HttpRequestException
        except HttpRequestException:
            LOG.error("Http request failed:%s, status code:%d" %
                      (req.text, req.status_code))
        except Exception as e:
            raise
