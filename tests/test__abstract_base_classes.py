from infi.unittest._compat import unittest_module as unittest
from infi.unittest import abstract_base_test, TestCase, TestLoader

#prevent nose from discovering this...
abstract_base_test.__test__ = False 

class AbstractBaseClassesTest(unittest.TestCase):
    def test__abstract_base_is_not_collected(self):
        @abstract_base_test
        class AbstractBaseTest(TestCase):
            def test__a(self):
                pass
            def test__b(self):
                pass
        class DerivedTest(AbstractBaseTest):
            def test__c(self):
                pass
        suite = TestLoader().loadTestsFromTestCase(AbstractBaseTest)
        self.assertEquals(suite._tests, [])
        suite = TestLoader().loadTestsFromTestCase(DerivedTest)
        self.assertEquals(len(suite._tests), 3)
        self.assertEqual(
            set([t._testMethodName for t in suite._tests]),
            set(['test__a', 'test__b', 'test__c'])
            )
