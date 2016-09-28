# coding=utf-8
from __future__ import unicode_literals
import hashlib
import json
import time

import requests

from utils import make_signature, check_signature
from languages import c_lang_config, cpp_lang_config, java_lang_config


token = hashlib.sha256("token").hexdigest()

c_src = r"""
#include <stdio.h>
int main(){
    int a, b;
    scanf("%d%d", &a, &b);
    printf("%d\n", a+b);
    return 0;
}
"""

cpp_src = r"""
#include <iostream>

using namespace std;

int main()
{
    int a,b;
    cin >> a >> b;
    cout << a+b << endl;
    return 0;
}
"""

java_src = r"""
import java.util.Scanner;
public class Main{
    public static void main(String[] args){
        Scanner in=new Scanner(System.in);
        int a=in.nextInt();
        int b=in.nextInt();
        System.out.println(a + b);
    }
}
"""


def compile_spj(src, spj_version, spj_config, test_case_id):
    data = make_signature(token=token,
                          src=src,
                          spj_version=spj_version,
                          spj_compile_config=spj_config,
                          test_case_id=test_case_id)
    r = requests.post("http://123.57.151.42:11235/compile_spj", data=json.dumps(data))
    data = r.json()
    check_signature(token=token, **data)
    result = json.loads(data["data"])
    if result["err"]:
        return result["data"]
    return json.loads(data["data"])["data"]


def judge(src, language_config, submission_id):
    data = make_signature(token=token,
                          language_config=language_config,
                          submission_id=submission_id,
                          src=src,
                          max_cpu_time=1000, max_memory=1024 * 1024 * 1024,
                          test_case_id="d8c460de943189a83bad166ec96d975d")
    r = requests.post("http://123.57.151.42:11235/judge", data=json.dumps(data))
    data = r.json()
    check_signature(token=token, **data)
    result = json.loads(data["data"])
    if result["err"]:
        return result["data"]
    return json.loads(data["data"])["data"]


def ping():
    data = make_signature(token=token)
    r = requests.post("http://123.57.151.42:11235/ping", data=json.dumps(data))

    data = r.json()
    check_signature(token=token, **data)
    result = json.loads(data["data"])
    if result["err"]:
        return result["data"]
    return json.loads(data["data"])["data"]


print ping()
print compile_spj(src=c_src, spj_version="2", spj_config=c_lang_config["spj"], test_case_id="d8c460de943189a83bad166ec96d975d")

print judge(src=c_src, language_config=c_lang_config, submission_id=str(int(time.time())))
time.sleep(2)
print judge(src=cpp_src, language_config=cpp_lang_config, submission_id=str(int(time.time())))
time.sleep(2)
print judge(src=java_src, language_config=java_lang_config, submission_id=str(int(time.time())))
