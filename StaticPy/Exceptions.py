#!/usr/bin/env python
#
# Copyright (c) 2013, Luke Southam <luke@devthe.com>
# All rights reserved. See LICENSE.md
"""
Exception Classes
"""

class BaseException(Exception):
    log = True
    def __str__(self):
        return repr(self.msg)

class NoCommandError(BaseException):
    def __init__(self, app):
        self.msg = "No command given"
        self.app = app

class UnknownCommandError(BaseException):
    def __init__(self, app, cmd):
        self.msg = "Unknown command %r" % cmd
        self.app = app

class InvalidDirectoryError(BaseException):
    def __init__(self, app, msg=None):
        self.msg = "Not a valid directory: %s" % app.path
        if msg:
            self.msg += "\n%s" % msg
        self.app = app