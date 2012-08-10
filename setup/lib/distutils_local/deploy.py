#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
"""test

Implements a Distutils 'test' command."""
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
__all__ = ['Deploy']

import sys
if sys.version_info < (3, 0):
    raise Exception("pytrader requires Python 3.0 or higher.")
import os
from distutils.core import Command
from distutils.errors import DistutilsOptionError
from distutils.util import get_platform

class Deploy(Command):
    description = "Place the distribution archive onto the distribution server."
    user_options = []

    def initialize_options(self):
        self.host = None
        self.path = None
        self.user = None
        
    def finalize_options(self):
        import getpass
        print("Transfer files to {0}:{1}".format(self.host, self.path))
        if self.user is None:
            self.user = getpass.getuser()
            user = input("Username ({}): ".format(self.user))
            if user:
                self.user = user

    def run(self):
        distdir = os.path.join(os.getcwd(), 'dist')
        args = ['/usr/bin/rsync', '-v']
        args.append(os.path.abspath(os.path.join(os.getcwd(), 'HEADER.html')))
        args.append(os.path.abspath(os.path.join(os.getcwd(), 'FOOTER.html')))
        args.extend([os.path.abspath(os.path.join(distdir, f)) for f in os.listdir(distdir)])
        args.append('{0}@{1}:{2}'.format(self.user, self.host, self.path))
        pid = subprocess.Popen(args)
        pid.wait()


