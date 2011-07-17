import unittest
from infi.unittest import TestCase as InfiTestCase
from infi.unittest import parameters
from infi.unittest import TestLoader, TestResult

class TestDescriptionTest(unittest.TestCase):
    def test__description(self):
        class MyTest(InfiTestCase):
            @parameters.iterate('a', [1])
            def setUp(self, a):
                super(MyTest, self).setUp()
                self.a = a
            @parameters.iterate('b', [4])
            def test(self, b):
                raise NotImplementedError()
        loader = TestLoader()
        suite = loader.loadTestsFromTestCase(MyTest)
        test = suite._tests[0]
        self.assertEquals(str(test), repr(test))
        self.assertEquals(str(test), "<test__description.MyTest[a=1].test(b=4)>")
