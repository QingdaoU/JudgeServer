# coding=utf-8
from __future__ import unicode_literals
import os
import json
import requests
import hashlib

from exception import JudgeServiceError
from utils import server_info, logger, token


class JudgeService(object):
    def __init__(self):
        # this container's ip and port, if these are not set, web server will think it's a linked container
        self.service_url = os.environ.get("service_url")

        # exists if docker link oj_web_server:oj_web_server
        self.service_discovery_host = os.environ.get("OJ_WEB_SERVER_PORT_8080_TCP_ADDR")
        self.service_discovery_port = os.environ.get("OJ_WEB_SERVER_PORT_8080_TCP_PORT")
        self.service_discovery_url = os.environ.get("service_discovery_url", "")

        if not self.service_discovery_url:
            if not (self.service_discovery_host and self.service_discovery_port):
                raise JudgeServiceError("service discovery host or port not found")
            else:
                self.service_discovery_url = "http://" + self.service_discovery_host + ":" + \
                                             str(self.service_discovery_port) + "/api/judge_server_heartbeat/"

    def _request(self, data):
        try:
            r = requests.post(self.service_discovery_url, data=json.dumps(data),
                              headers={"X-JUDGE-SERVER-TOKEN": token,
                                       "Content-Type": "application/json"}, timeout=5).json()
        except Exception as e:
            logger.exception(e)
            raise JudgeServiceError(e.message)
        if r["error"]:
            raise JudgeServiceError(r["data"])

    def heartbeat(self):
        data = server_info()
        data["action"] = "heartbeat"
        data["service_url"] = self.service_url
        self._request(data)


if __name__ == "__main__":
    try:
        service = JudgeService()
        service.heartbeat()
        exit(0)
    except Exception as e:
        logger.exception(e)
        exit(1)
