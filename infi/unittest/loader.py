from __future__ import absolute_import
import functools
import logging
import unittest
from .abstract_base import is_abstract_base_test
from .parameters import get_parameter_spec
from .parameters import NO_SPECS
from .test_filter import TestFilter
from .case import TestCase as InfiTestCase

class TestLoader(unittest.TestLoader):
    def discover(self, *args, **kwargs):
        test_filter = TestFilter.parse_filters(kwargs.pop('filters', None))
        return test_filter.filter(super(TestLoader, self).discover(*args, **kwargs))
    def loadTestsFromTestCase(self, testCaseClass):
        if is_abstract_base_test(testCaseClass):
            return self.suiteClass([])
        return self.suiteClass(self._get_test_cases(testCaseClass))
    def _get_test_cases(self, test_case_class):
        # a bit of copy-paste from the default implementation, unfortunately
        test_case_names = self.getTestCaseNames(test_case_class)
        if not test_case_names and hasattr(test_case_class, 'runTest'):
            test_case_names = ['runTest']

        return self._get_test_cases_by_names(test_case_class, test_case_names)
    def _get_test_cases_by_names(self, test_case_class, test_case_names):
        returned = []
        for test_case_name in test_case_names:
            returned.extend(self._get_multipled_cases(test_case_class, test_case_name))
        return returned
    def _get_multipled_cases(self, test_case_class, test_case_name):
        if issubclass(test_case_class, InfiTestCase):
            return test_case_class._get_all_cases(test_case_name)
        return [test_case_class(test_case_name)]
    def _iterate_setups(self, test_case_class):
        spec = get_parameter_spec(test_case_class.setUp)
        if spec is NO_SPECS:
            return [[]]
        return [[(spec.id, call)] for call in spec.iterate_calls()]

default_loader = TestLoader()
get_test_cases_from_test_class = default_loader._get_test_cases
