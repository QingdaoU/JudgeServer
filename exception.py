from __future__ import unicode_literals


class CompileError(Exception):
    pass


class SPJCompileError(CompileError):
    pass


class SignatureVerificationFailed(Exception):
    pass


class JudgeClientError(Exception):
    pass