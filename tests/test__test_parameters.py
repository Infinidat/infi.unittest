import itertools
import unittest
from infi.unittest import TestCase, TestLoader, parameters, TestResult
from test_utils import run_suite_assert_success

class ParametersTest(unittest.TestCase):
    def test__parameters(self):
        values_for_setup = [10, 20, 30]
        values_for_a = [1, 2, 3]
        values_for_b = [4, 5, 6]
        executed = set()
        expected = set(itertools.product(values_for_setup, values_for_a, values_for_b))
        expected.update((x, None, None) for x in values_for_setup)
        class SampleTest(TestCase):
            @parameters.iterate('param', values_for_setup)
            def setUp(self, param):
                super(SampleTest, self).setUp()
                self.setup_param = param
            @parameters.iterate('a', values_for_a)
            @parameters.iterate('b', values_for_b)
            def test_something(self, a, b):
                executed.add((self.setup_param, a, b))
            def test__no_params(self):
                executed.add((self.setup_param, None, None))
        suite = TestLoader().loadTestsFromTestCase(SampleTest)
        run_suite_assert_success(suite, len(expected))
        self.assertEquals(expected, executed)

