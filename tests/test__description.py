from __future__ import print_function
import functools
import os
import sys
import tempfile
import unittest
from infi.unittest import TestCase as InfiTestCase
from infi.unittest import parameters
from infi.unittest import TestLoader, TestResult
from infi.unittest import Call

class TestDescriptionTest(unittest.TestCase):
    def test__description(self):
        class MyTest(InfiTestCase):
            @parameters.iterate('a', [1])
            def setUp(self, a):
                super(MyTest, self).setUp()
                self.a = a
            @parameters.iterate('b', [4])
            def test(self, b):
                raise NotImplementedError()
        loader = TestLoader()
        suite = loader.loadTestsFromTestCase(MyTest)
        test = suite._tests[0]
        self.assertEquals("<test__description.{0}>".format(test), repr(test))
        self.assertEquals(str(test), "MyTest(a=1).test(b=4)")

class TestInformationTest(unittest.TestCase):
    def setUp(self):
        super(TestInformationTest, self).setUp()
        self.directory = tempfile.mkdtemp()
        self._old_sys_path = sys.path[:]
        self._old_sys_modules = sys.modules.copy()
        sys.path.append(self.directory)
        d = self.directory
        self.full_module_name = '__test_pkg__.a.b.c.module'
        package, module_name = self.full_module_name.rsplit(".", 1)
        for p in package.split("."):
            d = os.path.join(d, p)
            os.makedirs(d)
            with open(os.path.join(d, '__init__.py'), 'w'):
                pass
        with open(os.path.join(d, module_name + '.py'), 'w') as test_file:
            test_file.write(_TEST_FILE_TEMPLATE)
    def tearDown(self):
        sys.path[:] = self._old_sys_path
        sys.modules.clear()
        sys.modules.update(self._old_sys_modules)
        super(TestInformationTest, self).tearDown()
    def test__fields(self):
        from __test_pkg__.a.b.c.module import Test
        [test] = TestLoader().loadTestsFromTestCase(Test)
        self.assertEquals(test.get_module_base_name(), 'module')
        self.assertEquals(test.get_module_full_name(), self.full_module_name)
        self.assertEquals(test.get_setup_call(), Call())
        self.assertEquals(test.get_method_call(), Call())
        self.assertEquals(test.get_method_name(), 'test__a')
        self.assertEquals(test.get_class_name(), 'Test')
    def test__fields_of_parameterized_tests(self):
        from __test_pkg__.a.b.c.module import ParameterizedTest
        tests = TestLoader().loadTestsFromTestCase(ParameterizedTest)._tests
        self.assertEquals(len(tests), 9)
        test = tests[0]
        self.assertEquals(test.get_setup_call(), Call(a=1))
        self.assertEquals(test.get_method_call(), Call(b=1))
        self.assertEquals(test.get_filename(), os.path.join(self.directory, *self.full_module_name.split('.')) + '.py')
        self.assertEquals(test.get_method_name(), 'test__a')
        self.assertEquals(test.get_class_name(), 'ParameterizedTest')

_TEST_FILE_TEMPLATE = """
from infi.unittest import TestCase
from infi.unittest import parameters

class Test(TestCase):
    def test__a(self):
        raise NotImplementedError()
class ParameterizedTest(TestCase):
    @parameters.iterate('a', [1, 2, 3])
    def setUp(self):
        pass
    @parameters.iterate('b', [1, 2, 3])
    def test__a(self):
        raise NotImplementedError()
"""
