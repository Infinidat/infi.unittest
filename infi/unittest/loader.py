from __future__ import absolute_import
import functools
import unittest
from .parameters import get_parameter_spec

class TestLoader(unittest.TestLoader):
    def loadTestsFromTestCase(self, testCaseClass):
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
            returned.extend(self._multiply_test_case_parameters(test_case_class, test_case_name))
        return returned
    def _multiply_test_case_parameters(self, test_case_class, test_case_name):
        method = getattr(test_case_class, test_case_name)
        parameter_specs = get_parameter_spec(method)
        for setup_args, setup_kwargs in self._iterate_setup(test_case_class):
            for method_args, method_kwargs in parameter_specs.iterate_args_kwargs():
                test_case = test_case_class(test_case_name)
                setup_func = functools.partial(test_case.setUp, *setup_args, **setup_kwargs)
                teardown_func = test_case.tearDown
                method = functools.partial(
                    getattr(test_case, test_case_name),
                    *method_args,
                    **method_kwargs
                    )
                yield unittest.FunctionTestCase(method, setUp=setup_func, tearDown=teardown_func)
    def _iterate_setup(self, test_case_instance):
        return get_parameter_spec(test_case_instance.setUp).iterate_args_kwargs()

default_loader = TestLoader()
get_test_cases_from_test_class = default_loader._get_test_cases
