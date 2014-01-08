from infi.unittest._compat import unittest_module as unittest
from test_utils import get_sample_package_root
from test_utils import run_suite_assert_success
from test_utils import count_number_of_cases_in_directory
from infi.unittest import TestLoader

class TestDiscoveryTest(unittest.TestCase):
    def test__simple_discovery(self):
        loader = TestLoader()
        suite = loader.discover(get_sample_package_root())
        result = run_suite_assert_success(suite, count_number_of_cases_in_directory(get_sample_package_root()))
    def test__discovery_with_path(self):
        run_suite_assert_success(
            TestLoader().discover(get_sample_package_root(),
                                  filters=["test__python_operators:EqualityTest"]),
            2 * (3 + 3)
            )
    def test__discovery_by_parameters(self):
        run_suite_assert_success(
            TestLoader().discover(get_sample_package_root(),
                                  filters=["test__python_operators:EqualityTest[a=2].test__inequality[b=None]"]),
            2
            )
