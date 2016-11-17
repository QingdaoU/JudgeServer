# coding=utf-8
from __future__ import unicode_literals

import grp
import os
import pwd

JUDGER_WORKSPACE_BASE = "/judger_run"
LOG_BASE = "/log"

COMPILER_LOG_PATH = os.path.join(LOG_BASE, "compile.log").encode("utf-8")
JUDGER_RUN_LOG_PATH = os.path.join(LOG_BASE, "judger.log").encode("utf-8")

RUN_USER_UID = pwd.getpwnam("nobody").pw_uid
RUN_GROUP_GID = grp.getgrnam("nogroup").gr_gid

COMPILER_USER_UID = pwd.getpwnam("compiler").pw_uid
COMPILER_GROUP_GID = grp.getgrnam("compiler").gr_gid

TEST_CASE_DIR = "/test_case"
SPJ_SRC_DIR = "/spj"
SPJ_EXE_DIR = "/spj"

TOKEN_FILE_PATH = "/token.txt"
