#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
"""ERChime department acceptance test."""
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

__all__ = ["TestFixture"]

import sys
import unittest


class TestFixture(unittest.TestCase):
    """This is a particular type of TestCase that when executed will
    setup a test fixture.
    
    The order of execution for a fixture is:
    1. ``fixture.fixtureSetUp``
    2. ``fixture.__call__``
       a. ``cls.setUpClass``
       b. ``self.setUp``
       c. ``self.runTest``
       d. ``self.tearDown``
       e. cleanup function
       f. ``cls.tearDownClass``
    3. ``fixture.fixtureTearDown``
    
    This can be executed independently as a TestCase with the results
    being used by other test cases as necessary.
    
    Fixture will be torn down in reverse order of being setup.
    
    It is the fixture's responsibility to determine if the tear down
    should do anything. For example if ``fixtureSetUp`` failed on the
    first line then ``fixtureTearDown`` should not do anything.
    """
        
    def setUpFixture(self):
        """Create fixture specific pieces before this fixture is
        executed as a test. The setup in this method should not be
        required for successful completion of this test case, but
        should be needed for use as a fixture.
        """
        pass
    
    def tearDownFixture(self):
        """Cleanup everything that was setup by this fixture, and
        was left by the actual test case. The state of the system
        should be exactly as it was right before ``fixtureSetUp``
        is called.
        """
        pass
        
        
    

