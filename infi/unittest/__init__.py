from __future__ import absolute_import
__version__ = "0.0.3"
from .case import TestCase
from .loader import TestLoader
from .result import TestResult

defaultTestLoader = TestLoader


#verbatim imports from unittest
from unittest import __all__ as _available_from_original

from unittest import (
    FunctionTestCase,
    SkipTest,
    TestSuite,
    TextTestResult,
    TextTestRunner,
    expectedFailure,
    findTestCases,
    getTestCaseNames,
    installHandler,
    main,
    makeSuite,
    registerResult,
    removeHandler,
    removeResult,
    skip,
    skipIf,
    skipUnless,
    )

__all__ = list(_available_from_original)
__all__.extend(['params'])
