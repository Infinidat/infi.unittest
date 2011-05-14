from types import MethodType
from nose.plugins.base import Plugin
from nose.loader import TestLoader as NoseTestLoader
from .loader import TestLoader

class NosePlugin(Plugin):
    name = "infi"
    enabled = True
    score = 0
    def prepareTestLoader(self, loader):
        loader.loadTestsFromTestCase = self._get_patched_test_case_loader(loader)
    def _get_patched_test_case_loader(self, loader):
        def loadTestsFromTestCase(self, testCaseClass):
            cases = []
            plugins = self.config.plugins
            for case in plugins.loadTestsFromTestCase(testCaseClass):
                cases.append(case)
            cases.extend(TestLoader()._get_test_cases(testCaseClass))
            return self.suiteClass(cases)
        return MethodType(loadTestsFromTestCase, loader, type(loader))

