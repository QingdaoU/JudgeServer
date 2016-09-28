# coding=utf-8
from __future__ import unicode_literals
import hashlib
import json
import time

import requests

from utils import make_signature
from languages import c_lang_config, c_lang_spj_config, cpp_lang_config, java_lang_config


submission_id = str(int(time.time()))

c_config = c_lang_config

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
    while(1);
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


def judge():
    data = make_signature(token=token,
                          language_config=java_lang_config,
                          submission_id=submission_id,
                          src=java_src,
                          max_cpu_time=1000, max_memory=1024 * 1024 * 1024,
                          test_case_id="d28280c6f3c5ddeadfecc3956a52da3a")
    r = requests.post("http://123.57.151.42:11235/judge", data=json.dumps(data))
    print r.json()


def ping():
    r = requests.post("http://123.57.151.42:11235/ping", data=json.dumps({}))
    print r.json()

ping()
judge()
