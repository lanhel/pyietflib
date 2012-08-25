#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""`vCard Parameter <http://tools.ietf.org/html/rfc6350#section-5>`_"""
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
import string
import re

from rfc2045 import ContentType
import rfc5870
from rfc5646 import LanguageTag

__all__ = ['build_parameter']
__log__ = logging.getLogger(__name__)


iana_token_re = re.compile(r"""^[-a-zA-Z0-9]+$""", flags=re.VERBOSE)

x_name_re = re.compile(r"""^[xX]-[-a-zA-Z0-9]+$""", flags=re.VERBOSE)

class Parameter():
    """Defines parameters that are associated with a vCard property.
    
    Properties
    ----------
    name
        The name of the parameter.
    
    value
        The value for the parameter. The type will depend on the actual
        parameter.
    """
    def __init__(self, name, value, line=0, column=0):
        self.__name = name
        self.line = line
        self.column = column
        self.valuestr = value
        self.value = self.parse_value(value)

        delattr(self, 'line')
        delattr(self, 'column')
    
    def __str__(self):
        def escape(value):
            if isinstance(value, int):
                value = '{0:d}'.format(value)
            elif isinstance(value, float):
                value = '{0:f}'.format(value)
                value = value.rstrip('0')
                value = value.rstrip('.')
            elif ';' in value or ':' in value:
                value = '"{0}"'.format(value)
            return value
        
        ret = [';', self.name, '=']
        if isinstance(self.value, (str, int, float)):
            ret.append(escape(self.value))
        elif isinstance(self.value, list):
            ret.append(','.join([escape(v) for v in self.value]))
        else:
            ret.append(escape(str(self.value)))
        return ''.join(ret)
    
    def __eq__(self, o):
        if isinstance(o, Parameter):
            return (self.name == o.name and self.value == o.value)
        else:
            return False
    
    def parse_value(self, value):
        """Parse the string version of the value into a type appropriate
        for the parameter and return that new value."""
        return value
    
    def check_value(self, value):
        """Allows specific parameter types to check the value before it
        is set in the parameter. If the value is allowed then it is
        returned, otherwise `None` should be returned."""
        return value
    
    def raise_invalid_value(self, value):
        raise ValueError("Invalid value `{0}` for {1.name} parameter ({1.line}, {1.column}).".format(value, self))
    
    @property
    def name(self):
        return self.__name
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        def check_str(value):
            if '"' in value:
                ValueError("Invalid DQUOTE (\") character in parameter value {0}.", value)
            if [x for x in value if x not in string.printable]:
                ValueError("Invalid CTL character in parameter value {0}.", value)
        
        def check_value(value):
            if isinstance(value, str):
                check_str(value)
            elif isinstance(value, (float, int)):
                pass
            elif isinstance(value, (list, tuple)):
                ValueError("Nested iterables are not allowed parameter values {0}.", value)
        
        value = self.check_value(value)
        if value is None:
            self.raise_invalid_value(value)

        if isinstance(value, (list, tuple)):
            value = list(value)
            for v in value:
                check_value(v)
        else:
            check_value(value)
        
        self.__value = value


class AnyParam(Parameter):
    param_abnf = '''any-param  = (iana-token / x-name) "=" param-value *("," param-value)'''
    param_name = ''
    
    def parse_value(self, value):
        if not iana_token_re.match(self.name):
            raise ValueError("Invalid parameter name`{0.name}` ({0.line}, {0.column}).".format(self))
        #elif not x_name_re.match(self.name):
        #    raise ValueError("Invalid x-name parameter `{0.name}` ({0.line}, {0.column}).".format(self))
        return [v.strip('"') for v in value.split(',')]

class LanguageParam(Parameter):
    """`§ 5.1 <http://tools.ietf.org/html/rfc6350#section-5.1>`_
    
    c.f. `Language-Tag <http://tools.ietf.org/html/rfc5646#section-2>`_
    """
    param_abnf = '''language-param = "LANGUAGE=" Language-Tag'''
    param_name = 'LANGUAGE'
    
    def parse_value(self, value):
        try:
            return LanguageTag(value)
        except ValueError as err:
            self.raise_invalid_value(value)

    def check_value(self, value):
        if isinstance(value, str):
            value = LanguageTag(value)
        elif isinstance(value, LanguageTag):
            return value
        else:
            return None

class ValueParam(Parameter):
    """`§ 5.2 <http://tools.ietf.org/html/rfc6350#section-5.2>`_"""
    param_abnf = '''value-param = "VALUE=" value-type'''
    value_abnf = '''value-type = "text"
                                / "uri"
                                / "date"
                                / "time"
                                / "date-time"
                                / "date-and-or-time"
                                / "timestamp"
                                / "boolean"
                                / "integer"
                                / "float"
                                / "utc-offset"
                                / "language-tag"
                                / iana-token  ; registered as described in section 12
                                / x-name'''
    param_name = 'VALUE'
    valid_values = ("text", "uri", "date", "time", "date-time",
        "date-and-or-time", "timestamp", "boolean", "integer",
        "float", "utc-offset", "language-tag")
        
    def check_value(self, value):
        invalid = [v for v in value if v not in ValueParam.valid_values]
        invalid = [v for v in invalid if not x_name_re.match(v)]
        invalid = [v for v in invalid if not iana_token_re.match(v)]
        return value if len(invalid) == 0 else None


class PrefParam(Parameter):
    """`§ 5.3 <http://tools.ietf.org/html/rfc6350#section-5.3>`_"""
    param_abnf = '''pref-param = "PREF=" (1*2DIGIT / "100")
                ; An integer between 1 and 100.'''
    param_name = 'PREF'
    
    def parse_value(self, value):
        try:
            return int(value)
        except ValueError as err:
            errv = x.args[0].split()[-1].strip("'")
            self.raise_invalid_value(errv)
    
    def check_value(self, value):
        value = int(value)
        return value if value in range(1, 101) else None


class AltidParam(Parameter):
    """`§ 5.4 <http://tools.ietf.org/html/rfc6350#section-5.4>`_"""
    param_abnf = '''altid-param = "ALTID=" param-value'''
    param_name = 'ALTID'
    
    def parse_value(self, value):
        return value.strip('"')


class PidParam(Parameter):
    """`§ 5.5 <http://tools.ietf.org/html/rfc6350#section-5.5>`_"""
    param_abnf = '''pid-param = "PID=" pid-value *("," pid-value)'''
    value_abnf = '''pid-value = 1*DIGIT ["." 1*DIGIT]'''
    param_name = 'PID'
    
    def parse_value(self, value):
        try:
            return [float(v) for v in value.split(',')]
        except ValueError as err:
            errv = x.args[0].split()[-1].strip("'")
            self.raise_invalid_value(errv)
    
    def check_value(self, value):
        for v in value:
            if not isinstance(v, float):
                return None
        return value


class TypeParam(Parameter):
    """`§ 5.6 <http://tools.ietf.org/html/rfc6350#section-5.6>`_"""
    param_abnf = '''type-param = "TYPE=" type-value *("," type-value)'''
    value_abnf = '''type-value = "work"
                                / "home"
                                / type-param-tel
                                / type-param-related
                                / iana-token
                                / x-name
                        ; This is further defined in individual property sections.'''
    param_name = 'TYPE'
    valid_values = ('work', 'home',
        
        #type-param-tel
        "text", "voice", "fax", "cell", "video", "pager", "textphone",
        
        #type-param-releated
        "contact", "acquaintance", "friend", "met", "co-worker",
        "colleague", "co-resident", "neighbor", "child", "parent",
        "sibling", "spouse", "kin", "muse", "crush", "date",
        "sweetheart", "me", "agent", "emergency")
    
    def parse_value(self, value):
        return value.split(',')
    
    def check_value(self, value):
        invalid = [v for v in value if v not in TypeParam.valid_values]
        invalid = [v for v in invalid if not x_name_re.match(v)]
        invalid = [v for v in invalid if not iana_token_re.match(v)]
        return value if len(invalid) == 0 else None


class MediatypeParam(Parameter):
    """`§ 5.7 <http://tools.ietf.org/html/rfc6350#section-5.7>`_"""
    param_abnf = '''mediatype-param = "MEDIATYPE=" mediatype'''
    value_abnf = '''mediatype = type-name "/" subtype-name *( ";" attribute "=" value )
                            ; "attribute" and "value" are from [RFC2045]
                            ; "type-name" and "subtype-name" are from [RFC4288]'''
    param_name = 'MEDIATYPE'
    
    def parse_value(self, value):
        try:
            return ContentType(value)
        except ValueError as err:
            self.raise_invalid_value(value)

    def check_value(self, value):
        if isinstance(value, str):
            value = ContentType(value)
        elif isinstance(value, ContentType):
            return value
        else:
            return None


class CalscaleParam(Parameter):
    """`§ 5.8 <http://tools.ietf.org/html/rfc6350#section-5.8>`_"""
    param_abnf = '''calscale-param = "CALSCALE=" calscale-value'''
    value_abnf = '''calscale-value = "gregorian" / iana-token / x-name'''
    param_name = 'CALSCALE'
    
    def check_value(self, value):
        if value == 'gregorian' or x_name_re.match(value) or iana_token_re.match(value):
            return value
        else:
            return None

class SortAsParam(Parameter):
    """`§ 5.9 <http://tools.ietf.org/html/rfc6350#section-5.9>`_"""
    param_abnf = '''sort-as-param = "SORT-AS=" sort-as-value'''
    value_abnf = '''sort-as-value = param-value *("," param-value)'''
    param_name = 'SORT-AS'
    
    def parse_value(self, value):
        return [v.strip('"') for v in value.split(',')]


class GeoParam(Parameter):
    """`§ 5.10 <http://tools.ietf.org/html/rfc6350#section-5.10>`_"""
    param_abnf = '''geo-parameter = "GEO=" DQUOTE URI DQUOTE'''
    param_name = 'GEO'
    
    def parse_value(self, value):
        return rfc5870.geo_uri(value.strip('"'))

    def check_value(self, value):
        if isinstance(value, str):
            value = rfc5870.geo_uri(value)
        elif isinstance(value, rfc5870.geouri.GeoURI):
            return value
        else:
            return None


class TzParam(Parameter):
    """`§ 5.11 <http://tools.ietf.org/html/rfc6350#section-5.11>`_"""
    param_abnf = '''tz-parameter = "TZ=" (param-value / DQUOTE URI DQUOTE)'''
    param_name = 'TZ'
    
    def parse_value(self, value):
        return value.strip('"')


defined_params = dict([(c.param_name, c) for c in locals().values() if getattr(c, '__base__', None) == Parameter])


def build_parameter(name, value, line=0, column=0):
    c = defined_params.get(name.upper())
    if c:
        return c(c.param_name, value)
    else:
        return AnyParam(name, value)



