import unittest
from test_utils import run_suite_assert_success

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
        result = run_suite_assert_success(suite, 3)
    def test__is_subclass_of_unittest_testcase(self):
        from infi.unittest import TestCase
        self.assertTrue(issubclass(TestCase, unittest.TestCase))

