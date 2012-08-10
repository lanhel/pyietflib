#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
"""changeversion

Implements a Distutils 'changeversion' command."""
__author__ = ('Lance Finn Helsten',)
__version__ = '1.0.2'
__copyright__ = """Copyright 2011 Lance Finn Helsten (helsten@acm.org)"""
__license__ = """
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
__all__ = ['ChangeVersion']

import sys
if sys.version_info < (3, 0):
    raise Exception("pytrader requires Python 3.0 or higher.")
import os
import errno
import re
import logging
from distutils.core import Command
from distutils.errors import DistutilsOptionError
from distutils.util import get_platform

class ChangeVersion(Command):
    description = "Change first __version__ string in all python files where the version is in xx.yy.zz form."
    user_options = [
        ("newversion=", None, "New version for all package.")
    ]
    
    def initialize_options(self):
        self.oldversion = tuple(self.distribution.get_version().split('.'))
        self.newversion = None
        
    def finalize_options(self):
        if self.newversion is None:
            print("New version must be specified.")
            sys.exit(errno.EINVAL)
        self.newversion = tuple(self.newversion.split('.'))
        if len(self.newversion) < 2 or 3 < len(self.newversion):
            print("New version must be a xx.yy or xx.yy.zz format.")
            sys.exit(errno.EINVAL)
        if self.newversion < self.oldversion:
            print("New version must be greater than {{0}.{1}.{2}}.".format(self.oldversion))
            sys.exit(errno.EINVAL)
        self.srcpat = re.compile(r"""__version__\s*=\s*['"]{1,3}(\d{1,2}\.\d{1,2}(\.\d{1,2})?)['"]{1,3}\s*""", re.MULTILINE)
        if len(self.newversion) == 2:
            self.repl = """__version__ = '{0}.{1}'\n""".format(*self.newversion)
        else:
            self.repl = """__version__ = '{0}.{1}.{2}'\n""".format(*self.newversion)

    def run(self):
        for package in self.distribution.packages:
            self.walkdirs(package)
            self.walkdirs(os.path.join('test', package))
    
    def walkdirs(self, dir):
        for dirpath, dirnames, filenames in os.walk(os.path.abspath(dir)):
            filenames = [f for f in filenames if os.path.splitext(f)[1] == '.py']
            for f in filenames:
                path = os.path.join(dirpath, f)
                file = open(path, mode='r')
                contents = file.read()
                file.close()
                match = self.srcpat.search(contents)
                if match and tuple(match.groups()[0].split('.')) == self.oldversion:
                    contents = self.srcpat.sub(self.repl, contents)
                    file = open(path, mode='w')
                    file.write(contents)
                    file.close()
                elif match:
                    print("Invalid version {0} in {1}.".format(match.groups()[0], path), file=sys.stderr)


