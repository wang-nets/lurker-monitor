import requests
import json
from config import GLOBAL_CONFIG


class FalconApi(object):
    def __init__(self):
        self.endpoint = GLOBAL_CONFIG.FALCON_API_ENDPOINT
        self.username = GLOBAL_CONFIG.FALCON_USER
        self.password = GLOBAL_CONFIG.FALCON_PASSWORD

    def _auth_session(self):
        try:
            payload = {
                'name':self.username,
                'password':self.password
            }
            auth_api = '%s/api/v1/user/login' % self.endpoint
            req = requests.post(url=auth_api, data=payload)
            req.raise_for_status()
            json_data = req.json()
            return json_data['sig']
        except requests.HTTPError:
            pass
        except Exception as e:
            pass

    def add_host_to_hostgroup(self, host_list, hostgroup_id):
        try:
            if not isinstance(host_list, list):
                raise TypeError
            sig = self._auth_session()
            headers = {
                'Apitoken':json.dumps({'name':self.username, 'sig':sig}),
                'X-Forwarded-For':'127.0.0.1'
            }
            api = '%s/api/v1/hostgroup/host' % self.endpoint
            payload = {
                'Hosts':host_list,
                'HostGroupID':hostgroup_id
            }
            req = requests.post(url=api, data=payload, headers=headers)
            req.raise_for_status()
        except TypeError:
            pass
        except requests.HTTPError:
            pass
        except Exception as e:
            pass