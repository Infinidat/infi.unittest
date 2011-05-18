import unittest
from infi.unittest import parameters, TestLoader

class SetupParametersTest(unittest.TestCase):
    def test__setup_parameters(self):
        values = [1, 2, 3, 4]
        called = []
        class T(unittest.TestCase):
            @parameters.iterate('value', values)
            def setUp(self, value):
                super(T, self).setUp()
                self.value = value
            def test_something(self):
                called.append(self.value)
        suite = TestLoader().loadTestsFromTestCase(T)
        self.assertEquals(suite.countTestCases(), len(values))
        suite.run(unittest.TestResult())
        self.assertItemsEqual(values, called)
