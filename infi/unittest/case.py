from __future__ import absolute_import
import sys
import itertools
import platform
import unittest
from .parameters import get_parameter_spec
from .parameters import NO_SPEC_ID
from .python3_compat import iteritems

class TestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self._argument_bindings = {}
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
    def get_setup_parameters(self):
        return self._get_setup_kwargs()
    def get_parameters(self):
        return self._get_method_kwargs()
    def _bind_parameters(self, spec_id, kwargs):
        if spec_id is NO_SPEC_ID:
            return
        self._argument_bindings.setdefault(spec_id, {}).update(kwargs)
    def _get_parameter_binding(self, spec_id):
        return self._argument_bindings.get(spec_id, {})
    def _get_setup_kwargs(self):
        spec = get_parameter_spec(self.setUp)
        return self._get_parameter_binding(spec.id)
    def _get_method_kwargs(self):
        method = getattr(self, self._testMethodName, None)
        if method is None:
            return {}
        spec = get_parameter_spec(method)
        return self._get_parameter_binding(spec.id)

    @classmethod
    def _get_all_cases(cls, method_name):
        for setup_assignment_spec in cls._get_setup_assignment_specs():
            for method_assignment_spec in cls._get_method_assignment_specs(method_name):
                test_case = cls(method_name)
                for spec_id, kwargs in itertools.chain(setup_assignment_spec, method_assignment_spec):
                    test_case._bind_parameters(spec_id, kwargs)
                yield test_case
    @classmethod
    def _get_setup_assignment_specs(cls):
        setup_specs = [get_parameter_spec(setup)
                       for setup in cls._get_setups()]
        setup_specs_kwargs_sets = [list(spec.iterate_kwargs()) for spec in setup_specs]
        combinations = itertools.product(*setup_specs_kwargs_sets)

        for combination in combinations:
            yield [(setup_spec.id, kwargs) for setup_spec, kwargs in zip(setup_specs, combination)]
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
    def _get_method_assignment_specs(cls, method_name):
        method = getattr(cls, method_name)
        spec = get_parameter_spec(method)
        return [
            [(spec.id, kwargs)]
            for kwargs in spec.iterate_kwargs()
            ]
    def __repr__(self):
        return "<{0}.{1}>".format(self.get_module_full_name(), self)
    def __str__(self):
        returned = self.get_class_name()
        setup_kwargs = self._get_setup_kwargs()
        return "{0}{1}.{2}{3}".format(
            self.get_class_name(),
            self._get_kwargs_str_if_not_empty(self._get_setup_kwargs()),
            self.get_method_name(),
            self._get_kwargs_str_if_not_empty(self._get_method_kwargs()),
            )
    def _get_kwargs_str_if_not_empty(self, kwargs):
        if not kwargs:
            return ""
        return "({0})".format(self._get_kwargs_str(kwargs))
    def _get_kwargs_str(self, kwargs):
        return ', '.join(
            "{0}={1!r}".format(key, value) for key, value in iteritems(kwargs)
            )




