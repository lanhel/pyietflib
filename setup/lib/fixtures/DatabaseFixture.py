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

__all__ = ["DatabaseFixture"]

import sys
import os
import unittest
from .TestFixture import TestFixture
from erchime.ERChimeConfig import config
from erchime.model import *

DB_PATH = os.path.abspath('./build/acceptance/var/db/accept.db')

class DatabaseFixture(TestFixture):
    """This fixture will setup a common database structure for use in
    acceptance testing."""
    
    def tearDownFixture(self):
        if os.path.isfile(DB_PATH):
            os.remove(DB_PATH)

    def setUp(self):
        database.init_schema()
    
    def tearDown(self):
        pass
    
    def runTest(self):
        pass
        #self.assertTrue(os.path.isfile(DB_PATH))

