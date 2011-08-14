Introduction
------------
*infi.unittest* is a set of extensions for the standard *unittest* module provided by the Python standard library. It provides several improvements over the original implementation, described below.

Installation
------------
The installation is done in the ordinary way:
::

  python setup.py install

Features
--------

Test Parameters
===============

One of the most annoying things about *unittest* is that you cannot easily specify test parameters. If you have a test to test an API with parameters, and you want several cases, each testing a specific value which should work and has a meaning, this can be annoying, and breaks the DRY principle:
::

 >>> import unittest
 >>> class MyTest(unittest.TestCase):
 ...     def test__api_call_with_yellow(self):
 ...         self._test_api_call('yellow')
 ...     def test__api_call_with_orange(self):
 ...         self._test_api_call('orange')
 ...     def _test_api_call(self, color):
 ...         some_api(color) # test here... yuck!

When using infi.unittest, you get a slightly better way of doing this:
::

 >>> from infi.unittest import TestCase
 >>> from infi.unittest import parameters
 >>> class MyTest(TestCase):
 ...     @parameters.iterate('color', ['orange', 'yellow'])
 ...     def test__api_call(self, color):
 ...         some_api(color) # yay!

The above will construct one test case per possible value, thus separating the cases for each value. It is also possible to use multiple values, multiplying the psosibilities:
::

 >>> class MyTest(TestCase):
 ...     @parameters.iterate('a', [1, 2, 3])
 ...     @parameters.iterate('b', [4, 5, 6])
 ...     def test__some_api(self, a, b):
 ...         pass

For boolean flags, there exists a simpler way to iterate between options::

 >>> class MyTest(TestCase):
 ...     @parameters.toggle('a', 'b', 'c')
 ...     def test__something(self, a, b, c):
 ...         pass # will be called with all combinations of True/False for a, b, c
 
Fixture Parameters
==================
Sometimes you want to write a set of tests, where the *fixture* for running them needs to iterate over options. For instance, if we want to test a utility method over both old-style and new-style classes:
::

 >>> class OldStyle:
 ...     pass
 >>> class NewStyle(object):
 ...     pass
 >>> class TestOldStyle(TestCase):
 ...     def setUp(self):
 ...         super(TestOldStyle, self).setUp()
 ...         self.tested_obj = OldStyle()
 ...     def test__1(self):
 ...         # do something with self.tested_obj
 ...         pass
 ...     def test__2(self):
 ...         # do something with self.tested_obj
 ...         pass
 >>> class TestNewStyle(TestCase):
 ...     def setUp(self):
 ...         super(TestNewStyle, self).setUp()
 ...         self.tested_obj = NewStyle()
 ...     def test__1(self):
 ...         # do something with self.tested_obj
 ...         pass
 ...     def test__2(self):
 ...         # do something with self.tested_obj
 ...         pass

A somewher clever, although not very pretty, way of doing this is inheritance:

 >>> class _BaseTest(TestCase):
 ...     def test__1(self):
 ...         # do something with self.tested_obj
 ...         pass
 ...     def test__2(self):
 ...         # do something with self.tested_obj
 ...         pass
 >>> class OldStyleTest(_BaseTest):
 ...     def setUp(self):
 ...         super(OldStyleTest, self).setUp()
 ...         self.tested_obj = OldStyle()
 >>> class NewStyleTest(_BaseTest):
 ...     def setUp(self):
 ...         super(NewStyleTest, self).setUp()
 ...         self.tested_obj = NewStyle()

This is yucky, and some discovery methods will attempt to run _BaseTest as well (although prefixed with an underscore). *infi.unittest* solves this elegantly:

 >>> class Test(TestCase):
 ...     @parameters.iterate('obj', [NewStyle(), OldStyle()])
 ...     def setUp(self, obj):
 ...         super(Test, self).setUp()
 ...         self.tested_obj = obj
 ...     def test__1(self):
 ...         # do something with self.tested_obj
 ...         pass
 ...     def test__2(self):
 ...         # do something with self.tested_obj
 ...         pass

infi.unittest can even multiply across inheritence. This means that the following code will eventually test the cartesian product between [1, 2, 3] and [4, 5, 6]
::

 >>> class BaseTest(TestCase):
 ...     @parameters.iterate('param', [1, 2, 3])
 ...     def setUp(self, param):
 ...         super(BaseTest, self).setUp()
 ...         self.base_param = param
 >>> class DerivedTest(BaseTest):
 ...     @parameters.iterate('param', [4, 5, 6])
 ...     def setUp(self, param):
 ...         super(DerivedTest, self).param()
 ...         self.derived_param = param
 ...     def test(self):
 ...         self.do_something_with(self.base_param, self.derived_param)

Note that even the super() call to setUp doesn't need to bother with the parameter(s) - it gets automatically bound.
 
Nose Integration
================
*infi.unittest* breaks compatibility with the excellent `nose: <http://code.google.com/p/python-nose/>` tool, itprovides a plugin to restore that compatibility. Running nose with the **--with-infi** option will make it properly process infi unittests. Of course this isn't needed if you're not using any of the features added by infi.
