# coding=utf-8
from __future__ import unicode_literals
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
        "seccomp_rule": "c_cpp",
        "max_process_number": 5
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
    },
    "run": {
        "command": "/usr/bin/java -cp {exe_dir} -Xss1M -XX:MaxPermSize=16M -XX:PermSize=8M -Xms16M -Xmx{max_memory}k -Djava.awt.headless=true Main",
        "seccomp_rule": None,
        "max_process_number": -1
    }
}

submission_id = str(int(time.time()))

c_config = c_lang_config
c_config["spj_compile"]["version"] = "1027"
c_config["spj_compile"]["src"] = "#include<stdio.h>\nint main(){//哈哈哈哈\nwhile(1);return 0;}"

token = hashlib.sha256("token").hexdigest()


def judge():
    data = make_signature(token=token,
                          language_config=java_lang_config,
                          submission_id=submission_id,
                          src="\nimport java.util.Scanner;\npublic class Main{\n    public static void main(String[] args){\n        Scanner in=new Scanner(System.in);\n        int a=in.nextInt();\n        int b=in.nextInt();\n        System.out.println((a+b));  \n    }\n}",
                          max_cpu_time=1000, max_memory=1024 * 1024 * 1024,
                          test_case_id="d28280c6f3c5ddeadfecc3956a52da3a")
    r = requests.post("http://192.168.99.100:8080/judge", data=json.dumps(data))
    print r.json()


def ping():
    r = requests.post("http://192.168.99.100:8080/ping", data=json.dumps({}))
    print r.json()

ping()
judge()
