import os
import itertools
import unittest
from infi.unittest import TestCase as InfiTestCase
from infi.unittest import TestLoader
from infi.unittest import TestResult
from infi.unittest.parameters import iterate
from infi.unittest.parameters import get_parameter_spec
from infi.unittest.parameters import NO_SPECS

class Validator(object):
    def __init__(self, expected):
        super(Validator, self).__init__()
        self.expected = set(expected)
    def is_successful(self):
        return not self.expected

def get_test_and_validator():
    prefixes = [10, 20, 30]
    numbers1 = [2, 3, 4]
    numbers2 = [5, 6, 7]

    validator = Validator(itertools.product(prefixes, numbers1, numbers2))
    class ReturnedTest(InfiTestCase):
        @iterate('prefix', prefixes)
        def setUp(self, prefix):
            super(ReturnedTest, self).setUp()
            self.prefix = prefix
        @iterate('number1', numbers1)
        @iterate('number2', numbers2)
        def test(self, number1, number2):
            validator.expected.remove((self.prefix, number1, number2))
    return ReturnedTest, validator

def get_sample_package_root():
    return os.path.join(os.path.dirname(__file__), "..", "sample_test_packages")

def run_suite(suite):
    result = TestResult()
    suite.run(result)
    return result

def run_suite_assert_success(suite, num_tests):
    result = run_suite(suite)
    assert not result.failures
    assert not result.errors
    assert not result.skipped
    assert result.testsRun == num_tests, "{0} tests expected to run, but {1} actually run!".format(num_tests, result.testsRun)
    return result

def count_number_of_cases_in_directory(path):
    suite = unittest.TestLoader().discover(path)
    return _count_number_of_cases_in_suite(suite)

def _count_number_of_cases_in_suite(suite):
    returned = 0
    for test in suite._tests:
        if isinstance(test, unittest.TestSuite):
            returned += _count_number_of_cases_in_suite(test)
        else:
            num_setup_cases = _count_setups(test)
            num_method_cases = _count_cases_in_method(getattr(test, test._testMethodName))
            returned += num_setup_cases * num_method_cases
    return returned

def _count_setups(test):
    returned = 1
    for cls in test.__class__.__mro__:
        setup = getattr(cls, "setUp", None)
        if setup is None:
            continue
        returned *= _count_cases_in_method(setup)
    return returned

def _count_cases_in_method(method):
    returned = get_parameter_spec(method)
    if returned is NO_SPECS:
        return 1
    return len(list(returned.iterate_calls()))
