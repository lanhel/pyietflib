#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
"""REST2py acceptance tests."""
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
__docformat__ = "reStructuredText en"

from .SmokeAcceptSuite import *
from .SanityAcceptSuite import *
from .ShakedownAcceptSuite import *

def load_tests(loader, tests, pattern):
    if os.environ["REST2PY_TEST_LEVEL"] in ['smoke', 'sanity', 'shakedown']:
        return SmokeAcceptSuite()
    
    if os.environ["REST2PY_TEST_LEVEL"] in ['sanity', 'shakedown']:
        return SanityAcceptSuite()
    
    if os.environ["REST2PY_TEST_LEVEL"] in ['shakedown']:
        return ShakedownAcceptSuite()

