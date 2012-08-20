#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
"""PyIETFlib sanity acceptance test suite. This may be executed directly
to run all of the sanity tests against the `build` directory."""
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

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

class SanityAcceptSuite(unittest.TestSuite):
    """Sanity test suite."""
    def __init__(self):
        super().__init__()
        tl = unittest.defaultTestLoader
        pwd = os.path.dirname(__file__)
        for path in os.listdir(pwd):
            fpath = os.path.join(pwd, path)
            ipath = os.path.join(fpath, '__init__.py')
            if path.endswith('TestSuite') and os.path.isfile(ipath):
                m = __import__(path)
                for t in m.sanity_suite():
                    self.addTest(t)

if __name__ == '__main__':
    from TestSuite import utils

    utils.set_accept_level(utils.SANITY)
    suite = SanityAcceptSuite()
    unittest.TextTestRunner(verbosity=2).run(suite)


