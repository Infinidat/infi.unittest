import unittest
from infi.unittest import TestCase, TestLoader, parameters, TestResult

class ParametersTest(unittest.TestCase):
    def test__parameters(self):
        values_for_a = [1, 2, 3]
        values_for_b = [4, 5, 6]
        expected = [(a, b) for a in values_for_a for b in values_for_b]
        expected.append((None, None))
        executed = []
        class SampleTest(TestCase):
            @parameters.iterate('a', values_for_a)
            @parameters.iterate('b', values_for_b)
            def test_something(self, a, b):
                executed.append((a, b))
            def test__no_params(self):
                executed.append((None, None))
        suite = TestLoader().loadTestsFromTestCase(SampleTest)
        result = TestResult()
        suite.run(result)
        self.assertEquals(suite.countTestCases(), len(expected))
        self.assertEquals(len(result.failures), 0)
        self.assertEquals(len(result.errors), 0)
        self.assertEquals(result.testsRun, len(expected))
        self.assertEquals(set(expected), set(executed))

