import functools
import unittest

class ParameterizedTestCase(unittest.FunctionTestCase):
    def __init__(self, test_case, setup_args, setup_kwargs, method_name, method_args, method_kwargs):
        method = functools.partial(getattr(test_case, method_name), *method_args, **method_kwargs)
        setup = functools.partial(test_case.setUp, *setup_args, **setup_kwargs)
        super(ParameterizedTestCase, self).__init__(method, setUp=setup, tearDown=test_case.tearDown)
        self._setup_args = setup_args
        self._setup_kwargs = setup_kwargs
        self._method_name = method_name
        self._method_args = method_args
        self._method_kwargs = method_kwargs
        self._test_case = test_case
        self._test_case_name = test_case.__class__.__name__
    def __repr__(self):
        return "<{0}[{1}].{2}({3})>".format(
            self._test_case_name,
            self._arg_str(self._setup_args, self._setup_kwargs),
            self._method_name,
            self._arg_str(self._method_args, self._method_kwargs),
            )
    def _arg_str(self, args, kwargs):
        args = list(args)
        args.extend("{0}={1!r}".format(key, value) for key, value in kwargs.iteritems())
        return ", ".join(args)
    def __str__(self):
        return repr(self)
