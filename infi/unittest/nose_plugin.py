from nose.plugins.base import Plugin
from nose.loader import TestLoader as NoseTestLoader
from .loader import get_test_cases_from_test_class
from .python3_compat import create_instance_method

class NosePlugin(Plugin):
    name = "infi"
    enabled = True
    score = 0
    def configure(self, options, conf):
        super(NosePlugin, self).configure(options, conf)
        self.enabled = True
    def prepareTestLoader(self, loader):
        loader.loadTestsFromTestCase = self._get_patched_test_case_loader(loader)
    def _get_patched_test_case_loader(self, loader):
        def loadTestsFromTestCase(self, testCaseClass):
            cases = []
            plugins = self.config.plugins
            for case in plugins.loadTestsFromTestCase(testCaseClass):
                cases.append(case)
            cases.extend(get_test_cases_from_test_class(testCaseClass))
            return self.suiteClass(cases)
        return create_instance_method(loadTestsFromTestCase, loader)

