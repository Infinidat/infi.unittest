import itertools
from infi.unittest._compat import unittest_module as unittest
from infi.unittest import TestCase, TestLoader, parameters, TestResult, abstract_base_test
from test_utils import run_suite_assert_success, run_suite

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
    def test__toggle(self):
        expected = set((x, y) for x in [True, False] for y in [True, False])
        executed = set()
        class SampleTest(TestCase):
            @parameters.toggle('a', 'b')
            def test__parameters(self, a, b):
                executed.add((a, b))
        run_suite_assert_success(TestLoader().loadTestsFromTestCase(SampleTest), len(expected))
        self.assertEquals(expected, executed)
    def test__iterate_over_callable(self):
        sequence = range(10)
        expected = set(sequence)
        executed = set()
        already_called = {"value" : False}
        def get_sequence():
            assert not already_called['value']
            already_called['value'] = True
            return sequence
        class SampleTest(TestCase):
            @parameters.iterate('x', get_sequence)
            def test__x(self, x):
                executed.add(x)
        self.assertFalse(already_called['value'])
        run_suite_assert_success(TestLoader().loadTestsFromTestCase(SampleTest), len(expected))
        self.assertEquals(executed, expected)

class AccidentalUsageOnUnittestTest(unittest.TestCase):
    def test__accidental_usage(self):
        class MyTest(unittest.TestCase):
            @parameters.iterate('bla', [1, 2, 3])
            def test_1(self):
                pass
        result = run_suite(TestLoader().loadTestsFromTestCase(MyTest))
        self.assertEquals(result.testsRun, 1)
        self.assertEquals(len(result.errors), 1)
        self.assertIn("does not derive from infi.unittest.testcase", result.errors[0][1].lower())

class SetupParametersAcrossInheritenceTest(unittest.TestCase):
    def test__inheritence(self):
        base_setup_args_a = range(5)
        base_setup_args_b = range(7)
        derived_setup_args = range(3)
        expected = set(itertools.product(base_setup_args_a, base_setup_args_b, derived_setup_args))
        run = set()
        class Base(TestCase):
            @parameters.iterate('a', base_setup_args_a)
            @parameters.iterate('b', base_setup_args_b)
            def setUp(self, a, b):
                super(Base, self).setUp()
                self.base_param_a = a
                self.base_param_b = b
        class Derived(Base):
            @parameters.iterate('param', derived_setup_args)
            def setUp(self, param):
                super(Derived, self).setUp()
                self.derived_param = param
            def test(self):
                run.add((self.base_param_a, self.base_param_b, self.derived_param))
        run_suite_assert_success(TestLoader().loadTestsFromTestCase(Derived), len(expected))
        self.assertEquals(run, expected)

    def test__inheritence_abstract_bases(self):
        @abstract_base_test
        class Base1(TestCase):
            def setUp(self):
                super(Base1, self).setUp()
            def tearDown(self):
                super(Base1, self).tearDown()
            def test(self):
                pass
        @abstract_base_test
        class Base2(Base1):
            @parameters.iterate('iterator', [0, 1])
            def setUp(self, iterator):
                super(Base2, self).setUp()
            def tearDown(self):
                super(Base2, self).tearDown()
        class Derived(Base2):
            pass
        run_suite_assert_success(TestLoader().loadTestsFromTestCase(Derived), 2)
