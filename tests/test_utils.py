import os
import itertools
from infi.unittest import TestCase as InfiTestCase
from infi.unittest import TestLoader
from infi.unittest import TestResult
from infi.unittest.parameters import iterate

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

def run_suite_assert_success(suite, num_tests):
    result = TestResult()
    suite.run(result)
    assert not result.failures
    assert not result.errors
    assert not result.skipped
    assert result.testsRun == num_tests
    return result
