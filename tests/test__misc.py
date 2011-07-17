import unittest
from infi.unittest import TestCase as InfiTestCase
from infi.unittest import TestLoader as InfiTestLoader
from infi.unittest import parameters
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

class RepresentationTest(unittest.TestCase):
    def test__represnetation(self):
        class DummyTest(InfiTestCase):
            @parameters.iterate('x', [1, 2, 3])
            def setUp(self, x):
                super(DummyTest, self).setUp()
                self.x = x
            @parameters.iterate('y', [1, 2, 3])
            def test__something(self, y):
                raise NotImplementedError() # pragma: no cover
        loader = InfiTestLoader()
        suite = loader.loadTestsFromTestCase(DummyTest)
        self.assertEquals(suite.countTestCases(), 9)
        for case in suite:
            self.assertIsInstance(str(case), basestring)
            self.assertIsInstance(repr(case), basestring)
            import pdb
            pdb.set_trace()

