# coding=utf-8
from __future__ import unicode_literals

import hashlib
import json
import os
import shutil
import socket
import logging

import _judger
import psutil
import web

from compiler import Compiler
from config import JUDGER_WORKSPACE_BASE, TEST_CASE_DIR
from exception import TokenVerificationFailed, CompileError, SPJCompileError
from judge_client import JudgeClient

DEBUG = os.environ.get("judger_debug") == "1"


class InitSubmissionEnv(object):
    def __init__(self, judger_workspace, submission_id):
        self.path = os.path.join(judger_workspace, submission_id)

    def __enter__(self):
        os.mkdir(self.path)
        os.chmod(self.path, 0777)
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not DEBUG:
            shutil.rmtree(self.path, ignore_errors=True)


class JudgeServer(object):
    def _health_check(self):
        ver = _judger.VERSION
        return {"hostname": socket.gethostname(),
                "cpu": psutil.cpu_percent(),
                "cpu_core": psutil.cpu_count(),
                "memory": psutil.virtual_memory().percent,
                "judger_version": ((ver >> 16) & 0xff, (ver >> 8) & 0xff, ver & 0xff)}

    def pong(self):
        return self._health_check()

    @property
    def _token(self):
        t = os.getenv("judger_token")
        if not t:
            raise TokenVerificationFailed("token not set")
        return hashlib.sha256(t).hexdigest()

    def judge(self, language_config, submission_id, src, max_cpu_time, max_memory, test_case_id,
              spj_version=None, spj_config=None):
        # init
        compile_config = language_config["compile"]

        with InitSubmissionEnv(JUDGER_WORKSPACE_BASE, submission_id=str(submission_id)) as submission_dir:
            src_path = os.path.join(submission_dir, compile_config["src_name"])

            # write source code into file
            with open(src_path, "w") as f:
                f.write(src.encode("utf-8"))

            # compile source code, return exe file path
            exe_path = Compiler().compile(compile_config=compile_config,
                                          src_path=src_path,
                                          output_dir=submission_dir)

            judge_client = JudgeClient(run_config=language_config["run"],
                                       exe_path=exe_path,
                                       max_cpu_time=max_cpu_time,
                                       max_memory=max_memory,
                                       test_case_id=str(test_case_id),
                                       submission_dir=submission_dir,
                                       spj_version=str(spj_version),
                                       spj_config=spj_config)
            run_result = judge_client.run()
            return run_result

    def compile_spj(self, spj_version, src, spj_compile_config, test_case_id):
        spj_compile_config["src_name"] = spj_compile_config["src_name"].format(spj_version=spj_version)
        spj_compile_config["exe_name"] = spj_compile_config["exe_name"].format(spj_version=spj_version)

        spj_src_path = os.path.join(TEST_CASE_DIR, test_case_id, spj_compile_config["src_name"])

        # if spj source code not found, then write it into file
        if not os.path.exists(spj_src_path):
            with open(spj_src_path, "w") as f:
                f.write(src.encode("utf-8"))
        try:
            Compiler().compile(compile_config=spj_compile_config,
                               src_path=spj_src_path,
                               output_dir=os.path.join(TEST_CASE_DIR, test_case_id))
        # turn common CompileError into SPJCompileError
        except CompileError as e:
            raise SPJCompileError(e.message)
        return "success"

    def POST(self):
        token = web.ctx.env.get("HTTP_X_JUDGE_SERVER_TOKEN", None)
        try:
            if token != self._token:
                raise TokenVerificationFailed("invalid token")
            if web.data():
                data = json.loads(web.data())
            else:
                data = {}

            if web.ctx["path"] == "/judge":
                callback = self.judge
            elif web.ctx["path"] == "/ping":
                callback = self.pong
            elif web.ctx["path"] == "/compile_spj":
                callback = self.compile_spj
            else:
                return json.dumps({"err": "invalid-method", "data": None})
            return json.dumps({"err": None, "data": callback(**data)})
        except Exception as e:
            logging.exception(e)
            ret = dict()
            ret["err"] = e.__class__.__name__
            ret["data"] = e.message
            return json.dumps(ret)


urls = (
    "/judge", "JudgeServer",
    "/ping", "JudgeServer",
    "/compile_spj", "JudgeServer"
)

if not os.environ.get("judger_token"):
    raise TokenVerificationFailed("token not set")

app = web.application(urls, globals())
wsgiapp = app.wsgifunc()

# gunicorn -w 4 -b 0.0.0.0:8080 server:wsgiapp
if __name__ == "__main__":
    app.run()