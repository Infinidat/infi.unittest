from __future__ import absolute_import
import platform
from .__version__ import __version__
if platform.python_version() < '2.7':
    import unittest2 as _unittest
else:
    import unittest as _unittest

_available_from_original = _unittest.__all__
globals().update((name, getattr(_unittest, name)) for name in _available_from_original if not name.startswith("_"))

from . import parameters
from .case import TestCase
from .call import Call
from .loader import TestLoader
from .result import TestResult
from .abstract_base import abstract_base_test

from .exceptions import *

defaultTestLoader = TestLoader

