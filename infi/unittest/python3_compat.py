import platform
from types import MethodType

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
