# coding=utf-8
import hashlib
import json
import time

import requests

from utils import make_signature

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

c_config = c_lang_config
c_config["spj_compile"]["version"] = "1027"
c_config["spj_compile"]["src"] = "#include<stdio.h>\nint main(){//哈哈哈哈\nwhile(1);return 0;}"

token = hashlib.sha256("token").hexdigest()


def judge():
    data = make_signature(token=token,
                          language_config=c_lang_config,
                          submission_id=submission_id,
                          src="#include<stdio.h>\nint main(){//哈哈哈哈\nwhile(1);return 0;}",
                          max_cpu_time=1000, max_memory=1000 * 1024 * 1024,
                          test_case_id="d28280c6f3c5ddeadfecc3956a52da3a")
    r = requests.post("http://192.168.99.100:8080/judge", data=json.dumps(data), headers={"content-type": "application/json"})
    print r.text


def ping():
    r = requests.post("http://192.168.99.100:8080/ping", data=json.dumps({}), headers={"content-type": "application/json"})
    print r.text

ping()
judge()
