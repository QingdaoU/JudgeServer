# coding=utf-8
from __future__ import unicode_literals
import _judger
import psutil
import socket
import os
import logging


def server_info():
    ver = _judger.VERSION
    return {"hostname": socket.gethostname(),
            "cpu": psutil.cpu_percent(),
            "cpu_core": psutil.cpu_count(),
            "memory": psutil.virtual_memory().percent,
            "judger_version": ".".join([str((ver >> 16) & 0xff), str((ver >> 8) & 0xff), str(ver & 0xff)])}


def get_token():
    return os.environ.get("OJ_WEB_SERVER_ENV_judger_token") or os.environ.get("judger_token")


logger = logging.getLogger(__name__)
handler = logging.FileHandler("/log/judge_server.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.WARNING)