from __future__ import absolute_import
import unittest
from .parameters import get_parameter_spec

class TestLoader(unittest.TestLoader):
    def loadTestsFromTestCase(self, testCaseClass):
        # a bit of copy-paste from the default implementation, unfortunately
        test_case_names = self.getTestCaseNames(testCaseClass)
        if not test_case_names and hasattr(testCaseClass, 'runTest'):
            test_case_names = ['runTest']

        test_cases = self._get_test_cases(testCaseClass, test_case_names)
        return self.suiteClass(test_cases)
    def _get_test_cases(self, test_case_class, test_case_names):
        returned = []
        for test_case_name in test_case_names:
            returned.extend(self._multiply_test_case_parameters(test_case_class, test_case_name))
        return returned
    def _multiply_test_case_parameters(self, test_case_class, test_case_name):
        method = getattr(test_case_class, test_case_name)
        parameter_specs = get_parameter_spec(method)
        if parameter_specs is None:
            return [test_case_class(test_case_name)]
        return [
            test_case_class(test_case_name, args=args, kwargs=kwargs)
            for args, kwargs in parameter_specs.iterate_args_kwargs()
            ]
