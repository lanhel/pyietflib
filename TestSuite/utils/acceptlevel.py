#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
"""Provides acceptance testing level filtering."""
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
import functools

__all__ = ['set_accept_level', 'skip_unless_accept_level',
            'SMOKE', 'SANITY', 'SHAKEDOWN',
            'smoke_suite', 'sanity_suite', 'shakedown_suite']

SMOKE = 'smoke'
SANITY = 'sanity'
SHAKEDOWN = 'shakedown'

match_levels = {
    SMOKE:(SMOKE,),
    SANITY:(SMOKE, SANITY),
    SHAKEDOWN:(SMOKE, SANITY, SHAKEDOWN)
}

accept_level = SANITY

def set_accept_level(level):
    """Set the acceptance test level for all tests to one of `smoke`,
    `sanity`, or `shakedown`."""
    global accept_level
    if level not in match_levels.keys():
        raise ValueError("Invalid level: {0}.".format(level))
    accept_level = level

def skip_unless_accept_level(level):
    """Decorate the test method of a `unittest.TestCase` to allow
    for test filtering."""
    def decorator(test_item):
        if isinstance(test_item, type) and issubclass(test_item, unittest.TestCase):
            if level not in match_levels[accept_level]:
                test_item.__unittest_skip__ = True
                test_item.__unittest_skip_why__ = "Not used in current test level."
            return test_item
        elif callable(test_item):
            @functools.wraps(test_item)
            def level_wrapper(*args, **kwargs):
                if level in match_levels[accept_level]:
                    return test_item(*args, **kwargs)
                else:
                    raise unittest.SkipTest("Not used in current test level.")
            return level_wrapper
        else:
            raise ValueError("Unable to decorate.")
    return decorator


def load_accept_smoke():
    """Convinience function to load all the acceptance tests associated
    with the smoke level."""


def create_suite(levels, path, top_level_dir=None):
    """Load all the tests in `path` into a suite if they are in the given
    levels. All modules must be loadable from the `top_level_dir`, if this
    is not given then this will recursively climb the tree to find the top
    directory with an `__init__.py` file."""
    if isinstance(levels, str):
        levels = [levels]
    
    if top_level_dir is None:
        p = path
        pp = os.path.dirname(p)
        while os.path.isfile(os.path.join(pp, '__init__.py')):
            p = pp
            pp = os.path.dirname(p)
        top_level_dir = p
    
    suite = unittest.TestSuite()
    tl = unittest.defaultTestLoader
    
    for level in levels:
        set_accept_level(level)
        suite.addTest(tl.discover(path, pattern='accept_*', top_level_dir=top_level_dir))
        for match in match_levels[level]:
            suite.addTest(tl.discover(path, pattern=(match + '_*'), top_level_dir=top_level_dir))
    return suite

def smoke_suite(path, top_level_dir=None):
    """Convinience method for creating a suite of smoke level acceptance
    tests that are in the given `path`. All modules must be loadable from
    the `top_level_dir`, if this is not given then this will recursively
    climb the tree to find the top directory with an `__init__.py` file."""
    return create_suite(SMOKE, path, top_level_dir)

def sanity_suite(path, top_level_dir=None):
    """Convinience method for creating a suite of sanity level acceptance
    tests that are in the given `path`. All modules must be loadable from
    the `top_level_dir`, if this is not given then this will recursively
    climb the tree to find the top directory with an `__init__.py` file."""
    return create_suite(SANITY, path, top_level_dir)

def shakedown_suite(path, top_level_dir=None):
    """Convinience method for creating a suite of shakedown level acceptance
    tests that are in the given `path`. All modules must be loadable from
    the `top_level_dir`, if this is not given then this will recursively
    climb the tree to find the top directory with an `__init__.py` file."""
    return create_suite(SHAKEDOWN, path, top_level_dir)

