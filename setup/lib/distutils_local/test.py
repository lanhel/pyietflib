#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
"""Implements a Distutils 'test_unit' and 'test_accept' command."""
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
import sys
if sys.version_info < (3, 0):
    raise Exception("pytrader requires Python 3.0 or higher.")
import os
import io
import errno
import configparser
import shutil
import itertools
from importlib.abc import Finder, Loader
import re
import logging
import subprocess
import time
import unittest

__all__ = ['test_unit', 'test_accept']

try:
    import coverage
except ImportError:
    print("### Ned Batchelder coverage module missing.", file=sys.stderr)
    print("### Tests will proceed with no coverage report.", file=sys.stderr)

from distutils.core import Command
from distutils.errors import DistutilsOptionError, DistutilsArgError

from distutils.util import get_platform

class TestFinder(Finder, Loader):
    def __init__(self, testcommand):
        self.build_lib = testcommand.build_lib
        self.test_lib = testcommand.test_lib
    
    def find_module(self, fullname, path=None):
        print("-+-+-+-+", fullname, path)
        return None

    def load_module(self, fullname):
        return None

class __TestCommand(Command):    
    def initialize_options(self):
        self.suite = []
        self.debug = None
        self.bSetup = False
        self.bTeardown = False
        self.test_type = None
        self.pattern = None
        self.coverage = False
        self.test_suite = None
        self.test_src = None
        self.build_base = 'build'
        self.build_lib = None
        self.test_base = None
        self.test_lib = None
        self.scripts_base = None
    
    def finalize_options(self):        
        if self.test_type is None:
            raise ValueError("test_type must be set.")
        
        if self.pattern is None:
            self.pattern = self.test_type + "_*.py"
        
        if self.test_src is None:
            self.test_src = '{0}Suite'.format(self.test_type.title())
        
        if self.build_lib is None:
            self.build_lib = os.path.join(self.build_base, 'lib')
        
        if self.test_base is None:
            self.test_base = os.path.join(self.build_base, self.test_type)
        
        if self.test_lib is None:
            self.test_lib = os.path.join(self.test_base, 'lib')
        
        if self.scripts_base is None:
            self.scripts_base = os.path.join(self.build_base, "scripts-3.2")
        
        #Reset the module load path
        del sys.path[0]
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        sys.path.insert(0, os.path.abspath(self.build_lib))
        sys.path.insert(0, os.path.abspath(self.test_lib))
        
        #Setup build/test directory
        if os.path.isdir(self.test_base):
            shutil.rmtree(self.test_base)
        os.makedirs(self.test_base, exist_ok=True)
        os.makedirs(os.path.join(self.test_base, 'etc'), exist_ok=True)
        
        for dirpath, dirnames, filenames in os.walk(self.test_src):
            for d in dirnames:
                dst = os.path.join(self.test_lib, dirpath, d)
                if not os.path.exists(dst):
                    #print('creating', dst)
                    os.makedirs(dst, exist_ok=True)
            for f in filenames:
                src = os.path.join(dirpath, f)
                dst = os.path.join(self.test_lib, dirpath, f)
                if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
                    #print('copying', src, '->', dst)
                    shutil.copy2(src, dst)
        
        #Setup logging
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
            level=logging.NOTSET,
            filename=os.path.join(self.test_base, "logfile.log"))
        
        #Setup coverage
        if self.coverage:
            omit = []
            for dirpath, dirnames, filenames in os.walk(self.test_base):
                omit.append(os.path.join(dirpath, '*.py'))
            for dirpath, dirnames, filenames in os.walk(self.build_lib):
                omit.append(os.path.join(dirpath, '__init__.py'))
            self.cov = coverage.coverage(branch=True, config_file=True, omit=omit)
        else:
            self.cov = NoCoverage()
        
    def __tests(self, suite):
        ret = []
        for t in suite:
            if isinstance(t, unittest.TestSuite):
                ret.extend(self.__tests(t))
            else:
                ret.append(t)
        return ret
    
    def build_test_suite(self):
        #Clear the cache of anything to do with this build so it will reload.
        #If this is not done then strange ImportError are thrown.
        cacheclear = [i for i in sys.path_importer_cache
                        if os.path.abspath(i).startswith(os.getcwd())]
        for i in cacheclear:
            del sys.path_importer_cache[i]
        
        #Find all test suites to run
        if self.debug is None:
            self.cov.start()
            tl = unittest.TestLoader()
            self.suite = tl.discover(self.test_lib, pattern=self.pattern)
            self.cov.stop()
        else:
            if re.match(r"^.+\.test[^.]+$", self.debug):
                module, self.method = self.debug.rsplit('.', 1)
            else:
                module = self.debug
                self.method = "runTest"
            module = self.debug
            module = module.replace('.', '/')
            module = os.path.join(self.test_lib, module)
            if os.path.isfile(module + '.py'):
                self.method = "runTest"
            elif os.path.isfile(os.path.dirname(module) + '.py'):
                self.method = os.path.basename(module)
                module = os.path.dirname(module)
            else:
                print("Unknown module and method:", self.debug, file=sys.stderr)
                sys.exit(1)
            module = module.replace(self.test_lib + '/', '')
            module = module.replace('/', '.')
            module = '.'.join([self.test_base, module])
            module = __import__(module)
            
            self.suite = unittest.TestLoader().loadTestsFromModule(module)
            self.case = self.__tests(self.suite)
            self.case = [c for c in self.case if str(c).startswith(self.method)]
            assert len(self.case) >= 1, "Debug cannot handle multiple cases."
            if not self.case:
                raise DistutilsArgError("No test case chosen")
            self.case = self.case[0]
    
    def run_test_suite(self):
        #Run the tests
        if self.debug is None:
            self.cov.start()
            tr = unittest.TextTestRunner()
            tr.run(self.suite)
            self.cov.stop()
            self.cov.save()
            #self.cov.report()
            self.cov.xml_report(outfile='build/coverage.xml')
            self.cov.html_report(directory='build/htmlcov')
        else:
            import pdb
            db = pdb.Pdb()
            if self.bSetup:
                db.rcLines.append('b self.setUp')
            db.rcLines.append('b self.{0}'.format(self.method))
            if self.bTeardown:
                db.rcLines.append('b self.tearDown')
            db.rcLines.append('c')
            db.rcLines.append('l')
            db.runcall(self.case.debug)
    
    def run(self):
        self.build_test_suite()
        self.run_test_suite()


class test_unit(__TestCommand):
    description = "Run all unit and integration tests on the system."
    user_options = [
        ("suite=", "s", "Run specific test suite [default: all tests]."),
        ("debug=", "d", "Debug a specific test with preset breakpoints."),
        ("coverage", "c", "Turn on code coverage for the tests."),
        ("bSetup", None, "Add a breakpoint in setUp for debug."),
        ("bTeardown", None, "Add a breakpoint in tearDown for debug."),
    ]
    
    def initialize_options(self):
        super().initialize_options()
        self.test_type = "test"

    def finalize_options(self):
        super().finalize_options()
    
    def run(self):
        super().run()
            

class test_accept(__TestCommand):
    description = "Run all acceptance tests on the system."
    user_options = [
        ("suite=", "s", "Run specific test suite [default: all tests]."),
        ("level=", "l", "Test suite level to run: smoke, sanity, or shakedown."),
        ("debug=", "d", "Debug a specific test with preset breakpoints."),
        ("coverage", "c", "Turn on code coverage for the tests."),
        ("bSetup", None, "Add a breakpoint in setUp for debug."),
        ("bTeardown", None, "Add a breakpoint in tearDown for debug."),
    ]

    def initialize_options(self):
        super().initialize_options()
        self.level = "sanity"
        self.test_type = "accept"

    def finalize_options(self):
        if self.level not in ['smoke', 'sanity', 'shakedown']:
            raise DistutilsOptionError("Invalid test level: {0}".format(self.level))
        os.environ["PYIETFRFC_TEST_LEVEL"] = self.level
        self.pattern = '*AcceptSuite'
        super().finalize_options()
    
    def run(self):
        super().run()


class NoCoverage():
    """Class that duck types coverage but does not do anything."""
    def __init__(self, *argv, **kvarg): pass
    def analysis(self, morf): pass
    def analysis2(self, morf): pass
    def annotate(self, morfs=None, directory=None, ignore_errors=None, omit=None, include=None): pass
    def clear_exclude(which='exclude'): pass
    def combine(self): pass
    def erase(self): pass
    def exclude(self, regex, which='exclude'): pass
    def get_exclude_list(self, which='exclude'): pass
    def html_report(self, morfs=None, directory=None, ignore_errors=None, omit=None, include=None): pass
    def load(self): pass
    def report(self, morfs=None, show_missing=True, ignore_errors=None, file=None, omit=None, include=None): pass
    def save(self): pass
    def start(self): pass
    def stop(self): pass
    def sysinfo(self): pass
    def use_cache(self): pass
    def xml_report(morfs=None, outfile=None, ignore_errors=None, omit=None, include=None): pass
