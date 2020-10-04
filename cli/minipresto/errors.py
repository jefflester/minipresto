#!usr/bin/env/python3
# -*- coding: utf-8 -*-

import minipresto.utils as utils


class MiniprestoError(Exception):
    """Generic Minipresto exception class."""

    exit_code = 1

    def __init__(self, msg=""):
        if not msg:
            utils.handle_missing_param(locals().keys(), __init__.__name__)
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return self.msg


class UserError(MiniprestoError):
    """An exception that Minipresto can handle and show to the user.

    ### Parameters
    - `msg`: The message to log, and the raised exception's message.
    - `hint_msg`: User hint (optional). Should help the user figure out how to
      solve the problem.
    """

    exit_code = 2

    def __init__(self, msg="", hint_msg=""):
        if not msg:
            utils.handle_missing_param("msg", __init__.__name__)
        if hint_msg:
            super().__init__(f"User error: {msg}\nHint: {hint_msg}")
        super().__init__(f"User error: {msg}")
