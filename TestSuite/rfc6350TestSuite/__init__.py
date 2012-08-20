#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
"""IETF RFC 6350 vCard Format Specification unit test suite."""
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

import os
import unittest

from TestSuite import utils

def test_suite():
    return unittest.defaultTestLoader.discover(os.path.dirname(__file__), pattern='test_*')

def smoke_suite():
    suite = utils.smoke_suite(os.path.dirname(__file__))
    return suite

def sanity_suite():
    suite = utils.sanity_suite(os.path.dirname(__file__))
    return suite

def shakedown_suite():
    suite = utils.shakedown_suite(os.path.dirname(__file__))
    return suite

