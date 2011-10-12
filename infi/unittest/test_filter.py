from ast import literal_eval
import re
import bunch
import unittest
from .call import EMPTY_CALL, Call
from .case import TestCase as InfiTestCase
from .filter_syntax import FILTER_STRING_PATTERN
from .python3_compat import basestring, iteritems

class TestFilter(object):
    @classmethod
    def parse_filters(cls, s):
        if s is None:
            return NullFilter()
        if isinstance(s, basestring):
            return ModuleClassMethodFilter(s)
        return OrFilter([cls.parse_filters(item) for item in s])
    def filter(self, suite):
        return unittest.TestSuite(
            test for test in self._unfold(suite) if self._is_allowed(test)
            )
    def _unfold(self, suite):
        for x in suite:
            if isinstance(x, unittest.TestSuite):
                for y in self._unfold(x):
                    yield y
            else:
                yield x
    def _is_allowed(self, test):
        raise NotImplementedError()

class ModuleClassMethodFilter(TestFilter):
    def __init__(self, filter_string):
        super(TestFilter, self).__init__()
        self._filter_args = _parse_filter_string(filter_string)
    def _is_allowed(self, test):
        for field_name, getter in [
            ('module_name', self._get_test_module_name),
            ('class_name', self._get_test_class_name),
            ('method_name', self._get_test_method_name),
            ('setup_call', self._get_test_setup_call),
            ('method_call', self._get_test_method_call),
            ]:
            filter_value = self._filter_args[field_name]
            if filter_value is None:
                continue
            if filter_value != getter(test):
                return False
        return True
    def _get_test_module_name(self, test):
        return self._get_test_class(test).__module__
    def _get_test_class_name(self, test):
        return self._get_test_class(test).__name__
    def _get_test_class(self, test):
        return test.__class__
    def _get_test_method_name(self, test):
        return test._testMethodName
    def _get_test_setup_call(self, test):
        if isinstance(test, InfiTestCase):
            return test.get_setup_call()
        return EMPTY_CALL
    def _get_test_method_call(self, test):
        if isinstance(test, InfiTestCase):
            return test.get_method_call()
        return EMPTY_CALL

class OrFilter(TestFilter):
    def __init__(self, filters):
        super(OrFilter, self).__init__()
        self._filters = filters
    def _is_allowed(self, test):
        return all(f._is_allowed(test) for f in self._filters)

class NullFilter(TestFilter):
    def filter(self, suite):
        return suite

def _parse_filter_string(s):
    returned = bunch.Bunch(FILTER_STRING_PATTERN.match(s).groupdict())
    for key in returned:
        if not returned[key]:
            returned[key] = None
    for key in ['method_call', 'setup_call']:
        returned[key] = _parse_call_filter(returned[key])
    return returned

def _parse_call_filter(value):
    if value is None:
        return None
    assert value.startswith("[") and value.endswith("]")
    call_args = []
    call_kwargs = {}
    for arg_str in value[1:-1].split(","):
        if "=" in arg_str:
            key, value = arg_str.split("=", 1)
            call_kwargs[key] = literal_eval(value)
        else:
            call_args.append(literal_eval(arg_str))
            call_kwargs[arg_s]
    return CallSubsetPredicate(Call(*call_args, **call_kwargs))

class CallSubsetPredicate(object):
    def __init__(self, call):
        super(CallSubsetPredicate, self).__init__()
        self.call = call
    def __eq__(self, call):
        if not isinstance(call, Call):
            return False
        return call.args[:len(self.call.args)] == call.args and \
               all(call.kwargs[key] == value for key, value in iteritems(self.call.kwargs))
    def __ne__(self, call):
        return not self == call
