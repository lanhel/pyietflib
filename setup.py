#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#----------------------------------------------------------------------------
"""IETF RFC media type objects."""
__author__ = ('Lance Finn Helsten',)
__version__ = '1.0'
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
if sys.version_info < (3, 2):
    raise Exception("pyietfrfc requires Python 3.2 or higher.")

import os

import locale
locale.setlocale(locale.LC_ALL, '')

from distutils.core import setup
from distutils.command.build import build

sys.path.insert(0, os.path.abspath("setup/lib"))
from distutils_local import *
build.sub_commands.append(('build_docutils', build_docutils.has_docs))


#Do the distutils setup
setup(
    name='ietfrfc',
    version=__version__,
    author='Lance Finn Helsten',
    author_email='lanhel@flyingtitans.com',
	#maintainer='',
    #maintainer_email='',
    url='http://www.flyingtitans.com/products/rest2py',
    description='IETF RFC media type representations.',
    long_description=open('README.txt', encoding='ascii').read(),
    license="Apache License, Version 2.0",    
    #scripts=[],
    #data_files=[],
    packages=[
        'rfc5646',
        'rfc6350'
    ],
    #package_dir={'' : 'src'},
    package_data = {
#        'rest2py': ['locale/*', 'help/*.css', 'headers/*.yml']
#        'rest2py':          [],
#        'rest2py.headers':  ['*.yml'],
#        'rest2py.locale':   ['*.ico', '*.css', '*.xml', 'en/*.html'],
#        'rest2py.entities': ['en/*.html']
    },
    requires=[
        "docutils (>0.8)"
    ],
    provides=[
    ],
    cmdclass={
        "test":test_unit,
        "accept":test_accept,
        "build_docutils":build_docutils
    }
)


