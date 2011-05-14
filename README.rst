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

Nose Integration
================
*infi.unittest* breaks compatibility with the excellent `nose: <http://code.google.com/p/python-nose/>` tool, itprovides a plugin to restore that compatibility. Running nose with the **--with-infi** option will make it properly process infi unittests. Of course this isn't needed if you're not using any of the features added by infi.
