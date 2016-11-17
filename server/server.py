# coding=utf-8
from __future__ import unicode_literals

import json
import os
import shutil
import uuid

import web

from compiler import Compiler
from config import JUDGER_WORKSPACE_BASE, SPJ_SRC_DIR, SPJ_EXE_DIR
from exception import TokenVerificationFailed, CompileError, SPJCompileError,JudgeClientError
from judge_client import JudgeClient
from utils import server_info, logger, token


DEBUG = os.environ.get("judger_debug") == "1"


class InitSubmissionEnv(object):
    def __init__(self, judger_workspace, submission_id):
        self.path = os.path.join(judger_workspace, submission_id)

    def __enter__(self):
        try:
            os.mkdir(self.path)
            os.chmod(self.path, 0777)
        except Exception as e:
            logger.exception(e)
            raise JudgeClientError("failed to create runtime dir")
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not DEBUG:
            try:
                shutil.rmtree(self.path)
            except Exception as e:
                logger.exception(e)
                raise JudgeClientError("failed to clean runtime dir")


class JudgeServer(object):
    def pong(self):
        data = server_info()
        data["action"] = "pong"
        return data

    def judge(self, language_config, src, max_cpu_time, max_memory, test_case_id,
              spj_version=None, spj_config=None, spj_compile_config=None, spj_src=None, output=False):
        # init
        compile_config = language_config.get("compile")
        run_config = language_config["run"]
        submission_id = str(uuid.uuid4())

        if spj_version:
            self.compile_spj(spj_version=spj_version, src=spj_src,
                             spj_compile_config=spj_compile_config,
                             test_case_id=test_case_id)

        with InitSubmissionEnv(JUDGER_WORKSPACE_BASE, submission_id=str(submission_id)) as submission_dir:
            if compile_config:
                src_path = os.path.join(submission_dir, compile_config["src_name"])

                # write source code into file
                with open(src_path, "w") as f:
                    f.write(src.encode("utf-8"))

                # compile source code, return exe file path
                exe_path = Compiler().compile(compile_config=compile_config,
                                              src_path=src_path,
                                              output_dir=submission_dir)
            else:
                exe_path = os.path.join(submission_dir, run_config["exe_name"])
                with open(exe_path, "w") as f:
                    f.write(src.encode("utf-8"))

            judge_client = JudgeClient(run_config=language_config["run"],
                                       exe_path=exe_path,
                                       max_cpu_time=max_cpu_time,
                                       max_memory=max_memory,
                                       test_case_id=str(test_case_id),
                                       submission_dir=submission_dir,
                                       spj_version=spj_version,
                                       spj_config=spj_config,
                                       output=output)
            run_result = judge_client.run()

            return run_result

    def compile_spj(self, spj_version, src, spj_compile_config, test_case_id):
        spj_compile_config["src_name"] = spj_compile_config["src_name"].format(spj_version=spj_version)
        spj_compile_config["exe_name"] = spj_compile_config["exe_name"].format(spj_version=spj_version)

        spj_src_path = os.path.join(SPJ_SRC_DIR, spj_compile_config["src_name"])

        # if spj source code not found, then write it into file
        if not os.path.exists(spj_src_path):
            with open(spj_src_path, "w") as f:
                f.write(src.encode("utf-8"))
        try:
            Compiler().compile(compile_config=spj_compile_config,
                               src_path=spj_src_path,
                               output_dir=SPJ_EXE_DIR)
        # turn common CompileError into SPJCompileError
        except CompileError as e:
            raise SPJCompileError(e.message)
        return "success"

    def POST(self):
        _token = web.ctx.env.get("HTTP_X_JUDGE_SERVER_TOKEN", None)
        try:
            if _token != token:
                raise TokenVerificationFailed("invalid token")
            if web.data():
                try:
                    data = json.loads(web.data())
                except Exception as e:
                    logger.info(web.data())
                    return {"ret": "ServerError", "data": "invalid json"}
            else:
                data = {}

            if web.ctx["path"] == "/judge":
                callback = self.judge
            elif web.ctx["path"] == "/ping":
                callback = self.pong
            elif web.ctx["path"] == "/compile_spj":
                callback = self.compile_spj
            else:
                return json.dumps({"err": "InvalidMethod", "data": None})
            return json.dumps({"err": None, "data": callback(**data)})
        except (CompileError, TokenVerificationFailed, SPJCompileError, JudgeClientError) as e:
            logger.exception(e)
            ret = dict()
            ret["err"] = e.__class__.__name__
            ret["data"] = e.message
            return json.dumps(ret)
        except Exception as e:
            logger.exception(e)
            ret = dict()
            ret["err"] = "JudgeClientError"
            ret["data"] =e.__class__.__name__ + ":" + e.message
            return json.dumps(ret)


urls = (
    "/judge", "JudgeServer",
    "/ping", "JudgeServer",
    "/compile_spj", "JudgeServer"
)


if DEBUG:
    logger.info("DEBUG=ON")

app = web.application(urls, globals())
wsgiapp = app.wsgifunc()

# gunicorn -w 4 -b 0.0.0.0:8080 server:wsgiapp
if __name__ == "__main__":
    app.run()