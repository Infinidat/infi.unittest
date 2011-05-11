from __future__ import absolute_import
import unittest


class TestCase(unittest.TestCase):
    def __init__(self, methodName, args=(), kwargs=None):
        super(TestCase, self).__init__('_do__run') # we'll do the method logic here...
        self._method_name = methodName
        self._args = args
        if kwargs is None:
            kwargs = {}
        self._kwargs = kwargs
    def _do__run(self):
        getattr(self, self._method_name)(*self._args, **self._kwargs)
