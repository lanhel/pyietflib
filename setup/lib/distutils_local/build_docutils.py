#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
"""Implements a method of building reStructuredText through docutils."""
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
__all__ = ['build_docutils']

import sys
if sys.version_info < (3, 0):
    raise Exception("pytrader requires Python 3.0 or higher.")
import os
import shutil
import itertools
import subprocess
from distutils.core import Command

def doc_dirs(packages):
    """Given a list of package names find all directories that have one
    reStructuredText file with a '.rst' extension."""
    dirs = [p.replace('.', os.sep) for p in packages]
    dirs = [os.path.abspath(p) for p in dirs]
    dirs = [p for p in dirs if [f for f in os.listdir(p) if os.path.splitext(f)[1] == '.rst']]
    dirs = [os.path.relpath(d) for d in dirs]
    return dirs

def doc_paths(packages):
    """Given a list of package names find all the reStructuredText files
    with a '.rst' extension."""
    dirs = [p.replace('.', os.sep) for p in packages]
    dirs = [os.path.abspath(p) for p in dirs]
    files = [[os.path.join(p, f) for f in os.listdir(p)] for p in dirs]
    files = [f for f in itertools.chain(*files) if os.path.splitext(f)[1] == '.rst']
    files = [os.path.relpath(f) for f in files]
    return files

class build_docutils(Command):
    description = "Build documentation with Docutils."
    user_options = [
        ('build-base=', 'b', "base directory for build library"),
        ('build-lib=', None, "build directory for all distribution"),
        ('force', 'f', 'Build documentation ignoring timestamps.')
    ]
        
    def has_docs(self):
        return len(doc_paths(self.distribution.packages)) > 0

    def initialize_options(self):
        self.build_base = 'build'
        self.build_lib = None
        self.force = False

    def finalize_options(self):
        if self.build_lib is None:
            self.build_lib = os.path.join(self.build_base, 'lib')
    
    def run(self):
        args = ["rst2html.py",
                "--stylesheet", "help.css",
                "--link-stylesheet",
                "--traceback",
                "SRC_PATH_ARG_2",
                "DST_PATH_ARG_3"]
        
        #Process the reStructuredText files.
        try:
            for f in doc_paths(self.distribution.packages):
                src = os.path.abspath(f)
                dst = os.path.abspath(
                    os.path.join(self.build_lib, os.path.splitext(f)[0] + ".html"))
                if not os.path.isdir(os.path.dirname(dst)):
                    os.makedirs(os.path.dirname(dst))
                if self.force or not os.path.isfile(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
                    print("Docutils", f)
                    args[-2] = os.path.abspath(src)
                    args[-1] = os.path.abspath(dst)
                    ret = subprocess.call(args)
        except OSError as err:
            if err.errno == errno.ENOENT:
                print("error: Docutils missing.", file=sys.stderr)
            raise err
        
        #Copy CSS files
        if 'PYTHONDOCUTILSPACKAGE' in os.environ:
            docutil_css = os.path.join(os.environ['PYTHONDOCUTILSPACKAGE'], 'writers/html4css1/html4css1.css')
            for p in doc_dirs(self.distribution.packages):
                dst = os.path.join(self.build_lib, p, 'html4css1.css')
                print("Copy", dst)
                shutil.copyfile(docutil_css, dst)
        
        files = [[os.path.join(p, f) for f in os.listdir(p)]
                for p in doc_dirs(self.distribution.packages)]
        files = [f for f in itertools.chain(*files)]
        files = [f for f in files if os.path.isfile(f)]
        files = [f for f in files if os.path.splitext(f)[1] not in [".py", ".rst"]]
        files = [f for f in files if not os.path.basename(f).startswith('.')]
        for f in files:
            src = os.path.abspath(f)
            dst = os.path.abspath(os.path.join(self.build_lib, f))
            shutil.copyfile(src, dst)
        



