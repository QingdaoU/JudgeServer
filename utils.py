# coding=utf-8
from __future__ import unicode_literals

import json
import time
import hashlib

from exception import SignatureVerificationFailed


def make_signature(**kwargs):
    token = kwargs.pop("token")
    data = json.dumps(kwargs)
    timestamp = int(time.time())
    return data, hashlib.sha256(data + str(timestamp) + token).hexdigest(), timestamp


def check_signature(token, data, signature, timestamp):
    ts = int(time.time())
    if abs(timestamp - ts) > 5:
        raise SignatureVerificationFailed("Timestamp interval is too long")

    if hashlib.sha256(data + str(timestamp) + token).hexdigest() != signature:
        raise SignatureVerificationFailed("Wrong signature")