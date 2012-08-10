#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
"""REST2py shakedown acceptance test suite."""
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

import sys
import os
import unittest

import fixtures
from rest2pyAcceptSuite import *

class SanityAcceptSuite(unittest.TestSuite):
    """Sanity test suite."""
    
    test_fixtures = [
    ]
        
    test_suites = [
        rest2pyAcceptSuite.serverAcceptSuite.OrganizationContentTypeYAMLSuite,
        rest2pyAcceptSuite.serverAcceptSuite.OrganizationContentTypeHTMLSuite
    ]
    
    test_classes = [
    ]

    def __init__(self):
        super().__init__()
        tl = unittest.TestLoader()
        for suite in SmokeAcceptSuite.test_suites:
            self.addTest(suite())
        for _class in SmokeAcceptSuite.test_classes:
            suite = tl.loadTestsFromTestCase(_class)
            self.addTest(suite)
        
        
    def run(self, result):
        if os.environ["REST2PY_TEST_LEVEL"] in ['shakedown']:
            for fixture in SanityAcceptSuite.test_fixtures:
                if result.shouldStop:
                    return result
                fixture.setUpFixture()
                fixture(result)
            super().run(result)
            for fixture in reversed(SmokeAcceptSuite.test_fixtures):
                fixture.tearDownFixture()


