# coding=utf-8
import hashlib
import httplib
import json
import time
import xmlrpclib

from utils import make_signature, check_signature


class TimeoutHTTPConnection(httplib.HTTPConnection):
    def __init__(self, host, timeout=10):
        httplib.HTTPConnection.__init__(self, host, timeout=timeout)


class TimeoutTransport(xmlrpclib.Transport):
    def __init__(self, timeout=10, *args, **kwargs):
        xmlrpclib.Transport.__init__(self, *args, **kwargs)
        self.timeout = timeout

    def make_connection(self, host):
        conn = TimeoutHTTPConnection(host, self.timeout)
        return conn


class TimeoutServerProxy(xmlrpclib.ServerProxy):
    def __init__(self, uri, timeout=10, *args, **kwargs):
        kwargs['transport'] = TimeoutTransport(timeout=timeout, use_datetime=kwargs.get('use_datetime', 0))
        xmlrpclib.ServerProxy.__init__(self, uri, *args, **kwargs)


c_lang_config = {
    "name": "c",
    "compile": {
        "src_name": "main.c",
        "exe_name": "main",
        "max_cpu_time": 3000,
        "max_real_time": 5000,
        "max_memory": 128 * 1024 * 1024,
        "compile_command": "/usr/bin/gcc -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c99 -static {src_path} -lm -o {exe_path}",
    },
    "run": {
        "command": "{exe_path}",
        "seccomp_rule": "c_cpp"
    },
    "spj_compile": {
        "src_name": "spj-{spj_version}.c",
        "exe_name": "spj-{spj_version}",
        "max_cpu_time": 10000,
        "max_real_time": 20000,
        "max_memory": 1024 * 1024 * 1024,
        "compile_command": "/usr/bin/gcc -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c99 -static {src_path} -lm -o {exe_path}",
        # server should replace to real info
        "version": "1",
        "src": ""
    }
}

java_lang_config = {
    "name": "java",
    "compile": {
        "src_name": "Main.java",
        "exe_name": "Main",
        "max_cpu_time": 3000,
        "max_real_time": 5000,
        "max_memory": -1,
        "compile_command": "/usr/bin/javac {src_path} -d {exe_dir} -encoding UTF8"
    }
}

submission_id = str(int(time.time()))
spj_config = c_lang_config["spj_compile"]

s = TimeoutServerProxy("http://192.168.99.100:8080", timeout=30, allow_none=True)

c_config = c_lang_config
c_config["spj_compile"]["version"] = "1025"
c_config["spj_compile"]["src"] = "#include<stdio.h>\nint main(){//哈哈哈哈\nreturn 0;}"


token = hashlib.sha256("token").hexdigest()


def pong():
    data, signature, timestamp = s.pong()
    # check_signature(token=token, data=data, signature=signature, timestamp=timestamp)
    print json.loads(data)


def judge():
    data, signature, timestamp = s.judge(*make_signature(token=token,
                                                         language_config=c_lang_config,
                                                         submission_id=submission_id,
                                                         src="#include<stdio.h>\nint main(){//哈哈哈哈\nreturn 0;}",
                                                         max_cpu_time=1000, max_memory=1000, test_case_id="1"))

    # check_signature(token=token, data=data, signature=signature, timestamp=timestamp)
    print json.loads(data)


pong()
judge()