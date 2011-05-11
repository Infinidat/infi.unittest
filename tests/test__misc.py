import unittest

class TestImportsFromUnittestStillWork(unittest.TestCase):
    def test__imports_still_work(self):
        from unittest import __all__ as available_from_unittest
        for name in available_from_unittest:
            try:
                exec "from infi.unittest import {}".format(name)
            except ImportError:
                self.fail("Name {!r} is not importable!".format(name))


class TestBackwardCompatibility(unittest.TestCase):
    def test__is_backwards_compatible(self):
        from infi.unittest import TestCase
        expected = ['a', 'b', 'c']
        run = []
        class SampleTest(TestCase):
            def test__a(self):
                run.append('a')
            def test__b(self):
                run.append('b')
            def test__c(self):
                run.append('c')
        suite = unittest.TestLoader().loadTestsFromTestCase(SampleTest)
        result = unittest.TestResult()
        suite.run(result)
        self.assertEquals(result.failures, [])
        self.assertEquals(result.errors, [])
        self.assertEquals(result.testsRun, 3)
        self.assertEquals(set(run), set(expected))
    def test__is_subclass_of_unittest_testcase(self):
        from infi.unittest import TestCase
        self.assertTrue(issubclass(TestCase, unittest.TestCase))

