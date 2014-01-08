from infi.unittest._compat import unittest_module as unittest
from infi.unittest.test_filter import TestFilter
from infi.unittest import Call

class TestFilterTest(unittest.TestCase):
    def _assert_matches(self, pattern, **fields):
        filter = TestFilter.parse_filters(pattern)
        filter_args = filter._filter_args
        for key, value in filter_args.items():
            expected_value = fields.pop(key, None)
            self.assertEquals(value, expected_value)
        self.assertEquals(fields, {})
    def test__patterns(self):
        self._assert_matches("test__a.test__b:A.b",
                             module_name="test__a.test__b",
                             class_name="A",
                             method_name="b")
        self._assert_matches("test__a.test__b",
                             module_name="test__a.test__b")
    def test__args_patterns(self):
        self._assert_matches("test__python_operators:EqualityTest[a=2].test__inequality[b=None]",
                             module_name="test__python_operators",
                             class_name="EqualityTest",
                             setup_call=Call(a=2),
                             method_name="test__inequality",
                             method_call=Call(b=None)
                             )
        self._assert_matches("test__a:A[x=30].a[y=None]",
                             module_name="test__a",
                             class_name="A",
                             setup_call=Call(x=30),
                             method_name="a",
                             method_call=Call(y=None))
