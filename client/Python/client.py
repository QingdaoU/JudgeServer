# coding=utf-8
from __future__ import unicode_literals

import hashlib
import json

import requests

from languages import c_lang_config, cpp_lang_config, java_lang_config, c_lang_spj_config, c_lang_spj_compile


class JudgeServerClientError(Exception):
    pass


class JudgeServerClient(object):
    def __init__(self, token, server_base_url):
        self.token = hashlib.sha256(token).hexdigest()
        self.server_base_url = server_base_url.rstrip("/")

    def _request(self, url, data=None):
        kwargs = {"headers": {"X-Judge-Server-Token": self.token}}
        if data:
            kwargs["data"] = json.dumps(data)
        try:
            return requests.post(url, **kwargs).json()
        except Exception as e:
            raise JudgeServerClientError(e.message)

    def ping(self):
        return self._request(self.server_base_url + "/ping")

    def judge(self, src, language_config, max_cpu_time, max_memory, test_case_id, spj_version=None, spj_config=None):
        data = {"language_config": language_config,
                "src": src,
                "max_cpu_time": max_cpu_time,
                "max_memory": max_memory,
                "test_case_id": test_case_id,
                "spj_version": spj_version,
                "spj_config": spj_config}
        return self._request(self.server_base_url + "/judge", data=data)

    def compile_spj(self, src, spj_version, spj_compile_config, test_case_id):
        data = {"src": src, "spj_version": spj_version,
                "spj_compile_config": spj_compile_config, "test_case_id": test_case_id}
        return self._request(self.server_base_url + "/compile_spj", data=data)


if __name__ == "__main__":
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

    c_spj_src = r"""
    #include <stdio.h>
    int main(){
        return 1;
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

    client = JudgeServerClient(token="token", server_base_url="http://123.57.151.42:12358")
    print client.ping(), "\n\n"
    print client.compile_spj(src=c_spj_src, spj_version="1", spj_compile_config=c_lang_spj_compile,
                             test_case_id="spj"), "\n\n"

    print client.judge(src=c_src, language_config=c_lang_config,
                       max_cpu_time=1000, max_memory=1024 * 1024 * 128,
                       test_case_id="normal"), "\n\n"

    print client.judge(src=cpp_src, language_config=cpp_lang_config,
                       max_cpu_time=1000, max_memory=1024 * 1024 * 128,
                       test_case_id="normal"), "\n\n"

    print client.judge(src=java_src, language_config=java_lang_config,
                       max_cpu_time=1000, max_memory=1024 * 1024 * 1024,
                       test_case_id="normal"), "\n\n"

    print client.judge(src=c_src, language_config=c_lang_config,
                       max_cpu_time=1000, max_memory=1024 * 1024 * 128,
                       test_case_id="spj",
                       spj_version="1", spj_config=c_lang_spj_config), "\n\n"
