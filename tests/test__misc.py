import unittest

class TestImportsFromUnittestStillWork(unittest.TestCase):
    def test__imports_still_work(self):
        from unittest import __all__ as available_from_unittest
        for name in available_from_unittest:
            try:
                exec "from infi.unittest import {}".format(name)
            except ImportError:
                self.fail("Name {!r} is not importable!".format(name))

