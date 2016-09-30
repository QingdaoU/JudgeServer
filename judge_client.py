# coding=utf-8
from __future__ import unicode_literals
import _judger
import psutil
import os
import json
import hashlib

from multiprocessing import Pool

from config import TEST_CASE_DIR, JUDGER_RUN_LOG_PATH, LOW_PRIVILEDGE_GID, LOW_PRIVILEDGE_UID
from exception import JudgeClientError


def _run(instance, test_case_file_id):
    return instance._judge_one(test_case_file_id)


class JudgeClient(object):
    def __init__(self, run_config, exe_path, max_cpu_time, max_memory, test_case_id, submission_dir):
        self._run_config = run_config
        self._exe_path = exe_path
        self._max_cpu_time = max_cpu_time
        self._max_memory = max_memory
        self._max_real_time = self._max_cpu_time * 3
        self._test_case_id = test_case_id
        self._test_case_dir = os.path.join(TEST_CASE_DIR, test_case_id)
        self._submission_dir = submission_dir

        self._pool = Pool(processes=psutil.cpu_count())
        self._test_case_info = self._load_test_case_info()

    def _load_test_case_info(self):
        try:
            with open(os.path.join(self._test_case_dir, "info")) as f:
                return json.loads(f.read())
        except IOError:
            raise JudgeClientError("Test case not found")
        except ValueError:
            raise JudgeClientError("Bad test case config")

    def _seccomp_rule_path(self, rule_name):
        if rule_name:
            return "/usr/lib/judger/librule_{rule_name}.so".format(rule_name=rule_name).encode("utf-8")

    def _compare_output(self, test_case_file_id):
        user_output_file = os.path.join(self._submission_dir, str(test_case_file_id) + ".out")
        try:
            f = open(user_output_file, "r")
        except Exception:
            return None, False
        output_md5 = hashlib.md5(f.read().rstrip()).hexdigest()
        return output_md5, output_md5 == self._test_case_info["test_cases"][str(test_case_file_id)]["striped_output_md5"]

    def _judge_one(self, test_case_file_id):
        in_file = os.path.join(self._test_case_dir, str(test_case_file_id) + ".in")
        out_file = os.path.join(self._submission_dir, str(test_case_file_id) + ".out")

        command = self._run_config["command"].format(exe_path=self._exe_path, exe_dir=os.path.dirname(self._exe_path),
                                                     max_memory=self._max_memory / 1024).split(" ")

        run_result = _judger.run(max_cpu_time=self._max_cpu_time,
                                 max_real_time=self._max_real_time,
                                 max_memory=self._max_memory,
                                 max_output_size=1024 * 1024 * 1024,
                                 max_process_number=self._run_config["max_process_number"],
                                 exe_path=command[0].encode("utf-8"),
                                 input_path=in_file,
                                 output_path=out_file,
                                 error_path=out_file,
                                 args=[item.encode("utf-8") for item in command[1::]],
                                 env=[("PATH=" + os.getenv("PATH")).encode("utf-8")],
                                 log_path=JUDGER_RUN_LOG_PATH,
                                 seccomp_rule_so_path=self._seccomp_rule_path(self._run_config["seccomp_rule"]),
                                 uid=LOW_PRIVILEDGE_UID,
                                 gid=LOW_PRIVILEDGE_GID)
        run_result["test_case"] = test_case_file_id

        # if progress exited normally, then we should check output result
        run_result["output_md5"] = None
        if run_result["result"] == 0:
            run_result["output_md5"], is_ac = self._compare_output(test_case_file_id)
            # -1 == Wrong Answer
            if not is_ac:
                run_result["result"] = -1

        return run_result

    def run(self):
        tmp_result = []
        result = []
        for _ in range(self._test_case_info["test_case_number"]):
            tmp_result.append(self._pool.apply_async(_run, (self, _ + 1)))
        self._pool.close()
        self._pool.join()
        for item in tmp_result:
            # exception will be raised, when get() is called
            # # http://stackoverflow.com/questions/22094852/how-to-catch-exceptions-in-workers-in-multiprocessing
            result.append(item.get())
        return result

    def __getstate__(self):
        # http://stackoverflow.com/questions/25382455/python-notimplementederror-pool-objects-cannot-be-passed-between-processes
        self_dict = self.__dict__.copy()
        del self_dict["_pool"]
        return self_dict
