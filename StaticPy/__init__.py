#!/usr/bin/env python
#
# Copyright (c) 2013, Luke Southam <luke@devthe.com>
# All rights reserved. See LICENSE.md
"""
StaticPy
"""
import os
import logging

from plumbum import cli

from Exceptions import *

__author__ = "Luke Southam <luke@devthe.com>"
__copyright__ = "Copyright 2013, DEVTHE.COM LIMITED"
__license__ = "The BSD 3-Clause License"
__status__ = "Development"


class App(cli.Application):
    PROGNAME = "StaticPy"
    VERSION = "0.1"

    def main(self, *args):
        if args:
            raise UnknownCommandError(self, args[0])
        if not self.nested_command:
            raise NoCommandError(self)

    @cli.switch("--loglevel", int)
    def set_log_level(self, level):
        """Sets the log-level of the logger"""
        logging.root.setLevel(level)

@App.subcommand("init")
class AppInit(cli.Application):

    def main(self, path):
        self._fix_path(path)
        self.static_file = os.path.join(path, '.static')

        self._restrict_double_init()
        self.save()
        print "Initailized asset db for: %s" % self.path

    def save(self):
        static = "{}\n"
        with open(self.static_file, 'w') as f:
            # Set up the assets db
            f.write(static)

    def _fix_path(self, path):
        self.path = os.path.abspath(path)
        if not os.path.isdir(self.path):
            # It's not a dir!
            raise InvalidDirectoryError(self)

    def _restrict_double_init(self):
        try:
           with open(self.static_file) as f: pass
           raise InvalidDirectoryError(self, msg="Asset db already set")
        except IOError as e:
           pass


if __name__ == '__main__':
    try:
        App.run()
    except Exception, e:
        if hasattr(e, 'log') and e.log:
            print e.msg + "\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
~~~~~~~~~~~~~~~~~~~~~\n"
            e.app.help()
        else:
            raise e