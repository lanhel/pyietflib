#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
"""ERChime database test case that contains common setup and teardown
utilities."""
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
import unittest
import logging

from erchime.model.Database import *

__all__ = ['DatabaseTestCase']
__log__ = logging.getLogger(__name__)

class DatabaseTestCase(unittest.TestCase):   
    """ERChime database test case base class that makes setUp/tearDown of
    database environment easier.
    
    setUp
    -----
    `super().setUp()` must be called from a subclass's `setUp()` to ensure
    the tables exist, and to full initialize the test case.
    
    tearDown
    --------
    `super().tearDown()` may be called from a subclass's `tearDown()`
    method. This will clean out any tables where data was inserted
    through the `insert` method.
    
    """

    def insert(self, table, values):
        """Insert a set of values into the given table. The values tuple
        must mach the table structure exactly.
        
        Parameters
        ----------
        table
            The name of the table to insert the values. This name will
            be adjusted as necessary for working with `sqlite3` and
            `PostgreSQL`.
        
        values
            A string for a single value, a tuple or a list that contains
            multiple values to be turned into the a SQL INSERT VALUES
            string.
        """
        table = database.schema_table(table)
        self.addCleanup(self.clean_table, table)
        if type(values) == str:
            stmt = "INSERT INTO {0} VALUES ('{1}')".format(table, values)
        elif type(values) == tuple:
            stmt = "INSERT INTO {0} VALUES {1}".format(table, str(values))
        elif type(values) == list:
            stmt = "INSERT INTO {0} VALUES {1}".format(table, str(tuple(values)))
        stmt = stmt.replace('None', 'NULL')
        database.engine.execute(stmt)
    
    def clean_table(self, table):
        """This will clean out all data in the database in preparation
        for the database to be initialized through the `setUp` method.
        """
        database.engine.execute("DELETE FROM {0}".format(table))
    
    def setUp(self):
        super().setUp()
        database.init_schema()
        
    def tearDown(self):
        super().tearDown()
    
