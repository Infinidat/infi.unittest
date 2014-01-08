import sys
import platform
from types import MethodType

if sys.version_info < (2, 7):
    import unittest2 as unittest_module
    PYTHON_2_7_OR_HIGHER = False
else:
    import unittest as unittest_module
    PYTHON_2_7_OR_HIGHER = True


IS_PY3 = (platform.python_version() >= '3')

if IS_PY3:
    iteritems = dict.items
    create_instance_method = MethodType
    def create_instance_method(method, obj):
        return MethodType(method, obj)
    basestring = str
    from functools import reduce
    from types import FunctionType as UnboundMethodType
else:
    iteritems = dict.iteritems
    def create_instance_method(method, obj):
        return MethodType(method, obj, type(obj))
    from __builtin__ import basestring
    from __builtin__ import reduce
    from types import UnboundMethodType

def items_list(dictionary):
    return list(iteritems(dictionary))
