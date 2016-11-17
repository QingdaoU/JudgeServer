# coding=utf-8
from __future__ import unicode_literals
import _judger
import psutil
import socket
import logging
import hashlib

from config import TOKEN_FILE_PATH
from exception import JudgeClientError


logger = logging.getLogger(__name__)
handler = logging.FileHandler("/log/judge_server.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.WARNING)


def server_info():
    ver = _judger.VERSION
    return {"hostname": socket.gethostname(),
            "cpu": psutil.cpu_percent(),
            "cpu_core": psutil.cpu_count(),
            "memory": psutil.virtual_memory().percent,
            "judger_version": ".".join([str((ver >> 16) & 0xff), str((ver >> 8) & 0xff), str(ver & 0xff)])}


def get_token():
    try:
        with open(TOKEN_FILE_PATH, "r") as f:
            return f.read().strip()
    except IOError:
        raise JudgeClientError("token.txt not found")


token = hashlib.sha256(get_token()).hexdigest()

