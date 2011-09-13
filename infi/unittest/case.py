from __future__ import absolute_import
import sys
import itertools
import platform
import unittest
from .call import EMPTY_CALL
from .parameters import get_parameter_spec
from .parameters import NO_SPEC_ID
from .python3_compat import iteritems

class TestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self._spec_call_bindings = {}
    def get_method_name(self):
        return self._testMethodName
    def get_class_name(self):
        return self.__class__.__name__
    def get_module_base_name(self):
        return self.get_module_full_name().rsplit(".", 1)[-1]
    def get_module_full_name(self):
        return self.__class__.__module__
    def get_filename(self):
        return sys.modules[self.__class__.__module__].__file__
    def _bind_spec(self, spec_id, call):
        assert spec_id is not NO_SPEC_ID
        self._spec_call_bindings[spec_id] = call
    def get_setup_call(self):
        spec = get_parameter_spec(self.setUp)
        return self._spec_call_bindings.get(spec.id, EMPTY_CALL)
    def get_method_call(self):
        method = getattr(self, self._testMethodName, None)
        if method is None:
            return EMPTY_CALL
        spec = get_parameter_spec(method)
        return self._spec_call_bindings.get(spec.id, EMPTY_CALL)
    @classmethod
    def _get_all_cases(cls, method_name):
        for setup_specs_and_calls in cls._get_setup_specs_and_calls():
            for method_specs_and_calls in cls._get_method_specs_and_calls(method_name):
                test_case = cls(method_name)
                for spec, call in itertools.chain(setup_specs_and_calls, method_specs_and_calls):
                    if spec.id is not NO_SPEC_ID:
                        test_case._bind_spec(spec.id, call)
                yield test_case
    @classmethod
    def _get_setup_specs_and_calls(cls):
        setup_specs = [get_parameter_spec(setup)
                       for setup in cls._get_setups()]
        setup_calls = [list(spec.iterate_calls()) for spec in setup_specs]
        combinations = itertools.product(*setup_calls)

        for combination in combinations:
            yield [(setup_spec, call) for setup_spec, call in zip(setup_specs, combination)]
    @classmethod
    def _get_setups(cls):
        returned = []
        for c in cls.__mro__:
            setup = getattr(c, "setUp", None)
            if setup is None:
                continue
            returned.append(setup)
        return returned
    @classmethod
    def _get_method_specs_and_calls(cls, method_name):
        method = getattr(cls, method_name)
        spec = get_parameter_spec(method)
        return [
            [(spec, call)]
            for call in spec.iterate_calls()
            ]
    def __repr__(self):
        return "<{0}.{1}>".format(self.get_module_full_name(), self)
    def __str__(self):
        returned = self.get_class_name()
        return "{0}{1}.{2}{3}".format(
            self.get_class_name(),
            self._get_call_str_if_not_empty(self.get_setup_call()),
            self.get_method_name(),
            self._get_call_str_if_not_empty(self.get_method_call()),
            )
    def _get_call_str_if_not_empty(self, call):
        if not call:
            return ""
        return str(call)




