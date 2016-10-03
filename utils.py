# coding=utf-8
from __future__ import unicode_literals
import _judger
import psutil
import socket
import os


def server_info():
    ver = _judger.VERSION
    return {"hostname": socket.gethostname(),
            "cpu": psutil.cpu_percent(),
            "cpu_core": psutil.cpu_count(),
            "memory": psutil.virtual_memory().percent,
            "judger_version": ((ver >> 16) & 0xff, (ver >> 8) & 0xff, ver & 0xff)}


def get_token():
    return os.environ.get("OJ_WEB_SERVER_ENV_judger_token") or os.environ.get("judger_token")