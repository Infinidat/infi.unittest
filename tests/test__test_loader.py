import itertools
import os
import sys
from infi.unittest._compat import unittest_module as unittest
from tempfile import mkdtemp
from test_utils import get_sample_package_root
from test_utils import run_suite_assert_success
from test_utils import count_number_of_cases_in_directory
from infi.unittest import TestLoader, TestResult

class LoadTestsFromNameTest(unittest.TestCase):
    def setUp(self):
        super(LoadTestsFromNameTest, self).setUp()
        self.root_dir = mkdtemp()
        self.test_dir_name = self._get_test_dir_name()
        self.test_dir = os.path.join(self.root_dir, self.test_dir_name)
        os.mkdir(self.test_dir)
        sys.path.append(self.root_dir)
        self.num_cases = 10
        with open(os.path.join(self.test_dir, "__init__.py"), "w"):
            pass
        with open(os.path.join(self.test_dir, 'sometest.py'), 'w') as f:
            f.write("""
from infi.unittest import TestCase
from infi.unittest import parameters

class SomeTest(TestCase):
    @parameters.iterate('x', {0})
    def test(self, x):
        pass
""".format(list(range(self.num_cases))))
    def _get_test_dir_name(self):
        for i in itertools.count():
            name = 'auto_test_dir_{0}'.format(i)
            if name not in sys.modules:
                return name
    def test__load_tests_from_name_class(self):
        self._test__load_tests_from_name('{0}.sometest.SomeTest'.format(self.test_dir_name))
    def test__load_tests_from_name_method(self):
        self._test__load_tests_from_name('{0}.sometest.SomeTest.test'.format(self.test_dir_name))
    def _test__load_tests_from_name(self, name):
        loader = TestLoader()
        suite = loader.loadTestsFromName(name)
        result = TestResult()
        suite.run(result)
        self.assertEquals(result.testsRun, self.num_cases)
        self.assertEquals(result.failures, [])
        self.assertEquals(result.errors, [])
