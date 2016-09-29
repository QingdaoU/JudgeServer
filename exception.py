from __future__ import unicode_literals


class CompileError(Exception):
    pass


class SPJCompileError(CompileError):
    pass


class TokenVerificationFailed(Exception):
    pass


class JudgeClientError(Exception):
    pass