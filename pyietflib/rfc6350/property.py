#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""`vCard Property <http://tools.ietf.org/html/rfc6350#section-6>`_"""
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
import datetime

from .parameter import *
from pyietflib.iso8601 import parse_iso8601

__all__ = ['property_from_contentline',
    'ADR', 'ANNIVERSARY', 'BDAY', 'BEGIN', 'CALADRURI', 'CALURI',
    'CATEGORIES', 'CLIENTPIDMAP', 'EMAIL', 'END', 'FBURL', 'FN',
    'GENDER', 'GEO', 'IMPP', 'KEY', 'KIND', 'LANG', 'LOGO', 'MEMBER',
    'N', 'NICKNAME', 'NOTE', 'ORG', 'PHOTO', 'PRODID', 'RELATED',
    'REV', 'ROLE', 'SOUND', 'SOURCE', 'TEL', 'TITLE', 'TZ', 'UID',
    'URL', 'XML',
    'ExtendedProperty', 'IANAProperty' ]
__log__ = logging.getLogger('rfc6350')


class URI():
    pass

class Language():
    pass

class Address():
    pass

class Property():
    """Defines a specific vCard property.
    
    Properties
    ----------
    name
        The name string as it would appear in the vCard.
        
    value
        The value string as it would appear in the vCard.
    
    group
        The group name string as it would appear in the vCard.
    
    parameters
        The list of parameters on this property.
    """
    def __init__(self, value, group=None, params=None):
        self.__value = value
        self.__group = group
        self.__parameters = params if not None else []
        self.parse_value(value)
    
    def __str__(self):
        ret = []
        if self.group:
            ret.append("{0.group}")
        ret.append("{0.name}")
        for p in self.parameters:
            ret.append(str(p))
        ret.append(":{0.value}")
        ret.append("\r\n")
        ret = ''.join(ret)
        return ret.format(self)
    
    def __repr__(self):
        return "property.{0.name}({0.value}, group={0.group}, params={0.parameters})".format(self)
    
    def parse_value(self, value):
        """Parse the value and set properties on this object. The
        default will do nothing."""
        pass
    
    @property
    def group(self):
        return self.__group
    
    @property
    def name(self):
        return self.__class__.__name__
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        value = value.replace('\n', '\\n')
        value = value.replace('\r', '\\r')
        self.__value = value
        self.parse_value(value)
    
    @property
    def typed_value(self):
        pass
    
    @property
    def parameters(self):
        return self.__parameters

###
### §6.1 General Properties
###

class BEGIN(Property):
    """`§ 6.1.1 <http://tools.ietf.org/html/rfc6350#section-6.1.1>`_"""
    value_type = str
    cardinality = '1'
    parameters_allowed = ()
    
class END(Property):
    """`§ 6.1.2 <http://tools.ietf.org/html/rfc6350#section-6.1.2>`_"""
    value_type = str
    cardinality = '1'
    parameters_allowed = ()
    
class SOURCE(Property):
    """`§ 6.1.3 <http://tools.ietf.org/html/rfc6350#section-6.1.3>`_"""
    value_type = URI
    cardinality = '*'
    parameters_allowed = ('pid', 'pref', 'altid', 'mediatype', 'any')
    
class KIND(Property):
    """`§ 6.1.4 <http://tools.ietf.org/html/rfc6350#section-6.1.4>`_"""
    value_type = str
    cardinality = '*1'
    parameters_allowed = ('any',)
    
class XML(Property):
    """`§ 6.1.5 <http://tools.ietf.org/html/rfc6350#section-6.1.5>`_"""
    value_type = str
    cardinality = '*'
    parameters_allowed = ('altid',)
    
###
### §6.2 Identification Properties
###

class FN(Property):
    """`§ 6.2.1 <http://tools.ietf.org/html/rfc6350#section-6.2.1>`_"""
    value_type = str
    cardinality = '1*'
    parameters_allowed = ('type', 'language', 'altid', 'pid', 'pref', 'any')
    
class N(Property):
    """`§ 6.2.2 <http://tools.ietf.org/html/rfc6350#section-6.2.2>`_
    Specifies the components of the object's name.
    
    The structured property value corresponds, in sequence, to the Family
    Names (also known as surnames), Given Names, Additional Names, Honorific
    Prefixes, and Honorific Suffixes.  The text components are separated
    by the SEMICOLON character (U+003B).  Individual text components can
    include multiple text values separated by the COMMA character (U+002C).
    
    This property is based on the semantics of the X.520 individual
    name attributes [CCITT.X520.1988].  The property SHOULD be present
    in the vCard object when the name of the object the vCard represents
    follows the X.520 model.
    """
    value_type = str
    cardinality = '1*'
    parameters_allowed = ('sort-as', 'language', 'altid', 'any')
    
class NICKNAME(Property):
    """`§ 6.2.3 <http://tools.ietf.org/html/rfc6350#section-6.2.3>`_"""
    value_type = str
    cardinality = '*'
    parameters_allowed = ('type', 'language', 'altid', 'pid', 'pref', 'any')
    
class PHOTO(Property):
    """`§ 6.2.4 <http://tools.ietf.org/html/rfc6350#section-6.2.4>`_"""
    value_type = URI
    cardinality = '*'
    parameters_allowed = ('altid', 'type', 'mediatype', 'pref', 'pid', 'any')
    
class BDAY(Property):
    """`§ 6.2.5 <http://tools.ietf.org/html/rfc6350#section-6.2.5>`_"""
    value_type = datetime.datetime
    cardinality = '*1'
    parameters_allowed = ('altid', 'calscale', 'any')
    
    def parse_value(self, value):
        self.date = parse_iso8601(value)[0]
    
class ANNIVERSARY(Property):
    """`§ 6.2.6 <http://tools.ietf.org/html/rfc6350#section-6.2.6>`_"""
    value_type = datetime.datetime
    cardinality = '*1'
    parameters_allowed = ('altid', 'calscale', 'any')
    
    def parse_value(self, value):
        self.date = parse_iso8601(value)[0]
    
class GENDER(Property):
    """`§ 6.2.7 <http://tools.ietf.org/html/rfc6350#section-6.2.7>`_"""
    value_type = str
    value_re = re.compile(r'(?ax)^(?P<code>[MFONU]?)(;(?P<identity>.+))?$', flags=re.ASCII|re.VERBOSE)
    cardinality = '1'
    parameters_allowed = ('any',)
    
    def parse_value(self, value):
        mo = self.value_re.match(value)
        if not mo:
            raise ValueError("Invalid GENDER value `{0}`.".format(value))
        self.code = mo.group("code")
        self.identity = mo.group("identity")
    
    
###
### §6.3 Delivery Addressing Properties
###
    
class ADR(Property):
    """`§ 6.3.1 <http://tools.ietf.org/html/rfc6350#section-6.3.1>`_"""
    value_type = Address
    cardinality = '*'
    parameters_allowed = ('label', 'language', 'geo', 'tz', 'altid', 'pid', 'pref', 'type', 'any')
    
###
### §6.4 Communications Properties
###

class TEL(Property):
    """`§ 6.4.1 <http://tools.ietf.org/html/rfc6350#section-6.4.1>`_"""
    value_type = URI
    cardinality = '*'
    parameters_allowed = ('type', 'pid', 'pref', 'altid', 'any')
    
class EMAIL(Property):
    """`§ 6.4.2 <http://tools.ietf.org/html/rfc6350#section-6.4.2>`_"""
    value_type = URI
    cardinality = '*'
    parameters_allowed = ('pid', 'pref', 'type', 'altid', 'any')
    
class IMPP(Property):
    """`§ 6.4.3 <http://tools.ietf.org/html/rfc6350#section-6.4.3>`_"""
    value_type = URI
    cardinality = '*'
    parameters_allowed = ('pid', 'pref', 'type', 'mediatype', 'altid', 'any')

###
### §6.5 Geographical Properties
###

class LANG(Property):
    """`§ 6.5.1 <http://tools.ietf.org/html/rfc6350#section-6.5.1>`_"""
    value_type = Language
    cardinality = '*'
    parameters_allowed = ('pid', 'pref', 'altid', 'type', 'any')
    
class TZ(Property):
    """`§ 6.5.2 <http://tools.ietf.org/html/rfc6350#section-6.5.2>`_"""
    value_type = str
    cardinality = '*'
    parameters_allowed = ('altid', 'pid', 'pref', 'type', 'mediatype', 'any')
    
class GEO(Property):
    """`§ 6.5.3 <http://tools.ietf.org/html/rfc6350#section-6.5.3>`_"""
    value_type = URI
    cardinality = '*'
    parameters_allowed = ('pid', 'pref', 'type', 'mediatype', 'altid', 'any')

###
### §6.6 Organizational Properties
###

class TITLE(Property):
    """`§ 6.6.1 <http://tools.ietf.org/html/rfc6350#section-6.6.1>`_"""
    value_type = str
    cardinality = '*'
    parameters_allowed = ('language', 'pid', 'pref', 'altid', 'type', 'any')

class ROLE(Property):
    """`§ 6.6.2 <http://tools.ietf.org/html/rfc6350#section-6.6.2>`_"""
    value_type = str
    cardinality = '*'
    parameters_allowed = ('language', 'pid', 'pref', 'altid', 'type', 'any')

class LOGO(Property):
    """`§ 6.6.3 <http://tools.ietf.org/html/rfc6350#section-6.6.3>`_"""
    value_type = URI
    cardinality = '*'
    parameters_allowed = ('language', 'pid', 'pref', 'altid', 'type', 'mediatype', 'any')

class ORG(Property):
    """`§ 6.6.4 <http://tools.ietf.org/html/rfc6350#section-6.6.4>`_
    Specifies the organizational namd and associated units.
    
    A single structured text value consisting of components separated by
    the SEMICOLON character (U+003B).
    """
    value_type = str
    cardinality = '*'
    parameters_allowed = ('sort-as', 'language', 'pid', 'pref', 'altid', 'type', 'any')

class MEMBER(Property):
    """`§ 6.6.5 <http://tools.ietf.org/html/rfc6350#section-6.6.5>`_"""
    value_type = URI
    cardinality = '*'
    parameters_allowed = ('pid', 'pref', 'altid', 'mediatype', 'any')
    required_property = (KIND, )

class RELATED(Property):
    """`§ 6.6.6 <http://tools.ietf.org/html/rfc6350#section-6.6.6>`_"""
    value_type = (URI, str)
    values_allowed = (
            "contact", "acquaintance", "friend", "met", "co-worker",
            "colleague", "co-resident", "neighbor", "child", "parent",
            "sibling", "spouse", "kin", "muse", "crush", "date",
            "sweetheart", "me", "agent", "emergency"
        )
    cardinality = '*'
    parameters_allowed = {
            URI:('pid', 'pref', 'altid', 'type', 'any', 'mediatype'),
            str:('pid', 'pref', 'altid', 'type', 'any', 'language')
        }

###
### §6.7 Explanatory Properties
###

class CATEGORIES(Property):
    """`§ 6.7.1 <http://tools.ietf.org/html/rfc6350#section-6.7.1>`_
    Specifies application category.
    
    One or more text values separated by a COMMA character (U+002C).
    """
    value_type = list
    cardinality = '*'
    parameters_allowed = ('pid', 'pref', 'type', 'altid', 'any')
    

class NOTE(Property):
    """`§ 6.7.2 <http://tools.ietf.org/html/rfc6350#section-6.7.2>`_"""
    value_type = str
    cardinality = '*'
    parameters_allowed = ('language', 'pid', 'pref', 'type', 'altid', 'any')

class PRODID(Property):
    """`§ 6.7.3 <http://tools.ietf.org/html/rfc6350#section-6.7.3>`_"""
    value_type = str
    cardinality = '*1'
    parameters_allowed = ('any',)

class REV(Property):
    """`§ 6.7.4 <http://tools.ietf.org/html/rfc6350#section-6.7.4>`_"""
    value_type = datetime.datetime
    cardinality = '*1'
    parameters_allowed = ('any',)

class SOUND(Property):
    """`§ 6.7.5 <http://tools.ietf.org/html/rfc6350#section-6.7.5>`_"""
    value_type = URI
    cardinality = '*'
    parameters_allowed = ('language', 'pid', 'pref', 'type', 'mediatype', 'altid', 'any')

class UID(Property):
    """`§ 6.7.6 <http://tools.ietf.org/html/rfc6350#section-6.7.6>`_
    """
    value_type = URI
    cardinality = '*1'
    parameters_allowed = ('any',)

class CLIENTPIDMAP(Property):
    """`§ 6.7.7 <http://tools.ietf.org/html/rfc6350#section-6.7.7>`_
    
    A semicolon-separated pair of values.  The first field is a small
    integer corresponding to the second field of a PID parameter
    instance.  The second field is a URI.  The "uuid" URN namespace
    defined in [RFC4122] is particularly well suited to this task,
    but other URI schemes MAY be used.
    """
    value_type = str
    value_match = re.compile(r'\d+;.+')
    cardinality = '*'
    parameters_allowed = ('any')

class URL(Property):
    """`§ 6.7.8 <http://tools.ietf.org/html/rfc6350#section-6.7.8>`_"""
    value_type = str
    cardinality = '1'
    parameters_allowed = ()

###
### §6.8 Security Properties
###

class KEY(Property):
    """`§ 6.8.1 <http://tools.ietf.org/html/rfc6350#section-6.8.1>`_"""
    value_type = str
    cardinality = '1'
    parameters_allowed = ()

###
### §6.9 Calendar Properties
###

class FBURL(Property):
    """`§ 6.9.1 <http://tools.ietf.org/html/rfc6350#section-6.9.1>`_"""
    value_type = str
    cardinality = '1'
    parameters_allowed = ()

class CALADRURI(Property):
    """`§ 6.9.2 <http://tools.ietf.org/html/rfc6350#section-6.9.2>`_"""
    value_type = str
    cardinality = '1'
    parameters_allowed = ()

class CALURI(Property):
    """`§ 6.9.3 <http://tools.ietf.org/html/rfc6350#section-6.9.3>`_"""
    value_type = str
    cardinality = '1'
    parameters_allowed = ()

###
### §6.10 Extended Properties
###

class ExtendedProperty(Property):
    """`§ 6.10 <http://tools.ietf.org/html/rfc6350#section-6.10>`_
    
    vCard extended property.
    """
    
    VALID_NAME = re.compile(r'[xX]-[-a-zA-Z0-9]+', flags=re.ASCII|re.VERBOSE)
    
    def __init__(self, name, *args, **argv):
        if not ExtendedProperty.VALID_NAME.match(name):
            raise ValueError("Invalid extended property name `{0}`".format(name))
        self.__name = name
        super().__init__(*args, **argv)
    
    def __repr__(self):
        return "property.ExtendedProperty({0.name}, {0.value}, group={0.group}, params={0.parameters})".format(self)
    
    @property
    def name(self):
        return self.__name

###
###
###


class IANAProperty(Property):
    """`§ 6.10 <http://tools.ietf.org/html/rfc6350#section-6.10>`_
    
    vCard IANA registered property.
    """
    
    VALID_NAME = re.compile(r'[-a-zA-Z0-9]+', flags=re.ASCII|re.VERBOSE)
    
    def __init__(self, name, *args, **argv):
        if not IANAProperty.VALID_NAME.match(name):
            raise ValueError("Invalid IANA property name `{0}`".format(name))
        self.__name = name
        super().__init__(*args, **argv)
    
    def __repr__(self):
        return "property.IANAProperty({0.name}, {0.value}, group={0.group}, params={0.parameters})".format(self)
    
    @property
    def name(self):
        return self.__name


###
### Utilty Functions
###

defined_properties = dict([(c.__name__, c) for c in locals().values() if getattr(c, '__base__', None) == Property])

contentline_re = re.compile(r"""^
    ((?P<group>[-a-zA-Z0-9]+)\.)?
    (?P<name>[-a-zA-Z0-9]+)
    (?P<params>(;[-a-zA-Z0-9]+=(([^";:]*)|("[^"]*"))*)*)
    (:(?P<value>.+))
    \r\n$""", flags=re.VERBOSE)

params_re = re.compile(r"""
    ;(?P<pname>[-a-zA-Z0-9]+)
    =(?P<pvalue>(([^";:]+)|("[^"]+")))
""", flags=re.VERBOSE)

def property_from_contentline(value, line=0):
    """This will parse a single vCard contentline and produce a property.
    
    The line `value` must have been unfolded prior to this call according
    to `RFC 6350 § 3.2 <http://tools.ietf.org/html/rfc6350#section-3.2>`_.
    
    If `value` is a `byte` object then it will be decoded from UTF-8 into
    a `str`.
    """
    if isinstance(value, bytes) or isinstance(value, bytearray):
        value = value.decode('UTF-8')
    if not isinstance(value, str):
        raise TypeError('Invalid type `{0}` for content-line[{1}]: "{2:.30s}...".'.format(type(value), line, value))
    
    # Parse the content-line
    mo = contentline_re.match(value)
    if not mo:
        raise ValueError('Unable to parse content-line[{0}]: "{1:.30s}...".'.format(line, value))
    
    group = mo.group('group')
    name = mo.group('name')
    value = mo.group('value')
    
    # Build the parameter list
    params = []
    params_start = mo.start('params')
    pmo = params_re.match(mo.group('params'))
    while pmo:
        pname = pmo.group('pname')
        pvalue = pmo.group('pvalue')
        start = params_start + pmo.start() + 1
        params.append(build_parameter(pname, pvalue, line=line, column=start))
        pmo = params_re.match(mo.group('params'), pmo.end())
    
    # Build the property
    if name in defined_properties:
        return defined_properties[name](value, group=group, params=params)
    elif name.lower().startswith('x-'):
        return ExtendedProperty(name, value, group=group, params=params)
    else:
        return IANAProperty(name, value, group=group, params=params)



