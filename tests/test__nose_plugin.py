from infi.unittest._compat import unittest_module as unittest
from infi.unittest._compat import PYTHON_2_7_OR_HIGHER
import sys
import forge
from infi.unittest import TestLoader, TestResult
from infi.unittest import nose_plugin
from test_utils import get_test_and_validator

class NosePluginTest(unittest.TestCase):
    def setUp(self):
        super(NosePluginTest, self).setUp()
        self.forge = forge.Forge()
    def tearDown(self):
        self.forge.verify()
        self.forge.restore_all_replacements()
        super(NosePluginTest, self).tearDown()
    def test__nose_plugin(self):
        test, validator = get_test_and_validator()

        plugin = nose_plugin.NosePlugin()
        fake_config = self.forge.create_sentinel(
            plugins = self.forge.create_wildcard_mock()
            )
        self.extra_test_called = False
        def extra_test():
            self.extra_test_called = True
        fake_config.plugins.loadTestsFromTestCase(forge.Is(test)).and_return([unittest.FunctionTestCase(extra_test)])

        self.forge.replay()
        regular_loader = unittest.TestLoader()
        # nose loaders have a link to the configuration
        regular_loader.config = fake_config
        plugin.prepareTestLoader(regular_loader)

        suite = regular_loader.loadTestsFromTestCase(test)
        self.assertFalse(self.extra_test_called)
        result = TestResult()
        suite.run(result)
        self.assertTrue(self.extra_test_called)
        self.assertTrue(validator.is_successful())
        self.assertEquals(result.failures, [])
        if PYTHON_2_7_OR_HIGHER:
            self.assertEquals(result.skipped, [])
        self.assertEquals(result.errors, [])
