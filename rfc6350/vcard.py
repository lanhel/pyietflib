#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""`vCard <http://tools.ietf.org/html/rfc6350>`_ object that contains
the information in structured form."""
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
    raise Exception("pyvcard requires Python 3.2 or higher.")
import logging
import re

from .property import *

__all__ = []
__log__ = logging.getLogger(__name__)


class vCard():
    """Defines a structured vCard in accordance with `RFC 6350: vCard
    Format Specification <http://tools.ietf.org/html/rfc6350>`_
    that defines version 4 vCard.
    """
    def __init__(self, version='4.0'):
        self.version = version
        self.__properties = []


