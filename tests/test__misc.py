from infi.unittest._compat import unittest_module as unittest
from infi.unittest._compat import reduce
from infi.unittest import TestCase as InfiTestCase
from infi.unittest import TestLoader as InfiTestLoader
from infi.unittest import parameters
from test_utils import run_suite_assert_success

class TestImportsFromUnittestStillWork(unittest.TestCase):
    def test__imports_still_work(self):
        from unittest import __all__ as available_from_unittest
        for name in available_from_unittest:
            try:
                exec("from infi.unittest import {0}".format(name))
            except ImportError:
                self.fail("Name {!r} is not importable!".format(name))


class TestBackwardCompatibility(unittest.TestCase):
    def test__is_backwards_compatible(self):
        expected = reduce(list.__add__,
                          (['setup', x, 'teardown'] for x in 'abc'),
                          [])
        run = []
        class SampleTest(InfiTestCase):
            def setUp(self):
                super(SampleTest, self).setUp()
                run.append('setup')
            def tearDown(self):
                run.append('teardown')
                super(SampleTest, self).tearDown()
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


