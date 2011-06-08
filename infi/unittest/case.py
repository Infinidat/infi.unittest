from __future__ import absolute_import
import itertools
import unittest
from .parameters import get_parameter_spec
from .parameters import NO_SPEC_ID

class TestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self._argument_bindings = {}
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
        setup_func = cls.setUp
        spec = get_parameter_spec(setup_func)
        return [
            [(spec.id, kwargs)]
            for kwargs in spec.iterate_kwargs()
            ]
    @classmethod
    def _get_method_assignment_specs(cls, method_name):
        method = getattr(cls, method_name)
        spec = get_parameter_spec(method)
        return [
            [(spec.id, kwargs)]
            for kwargs in spec.iterate_kwargs()
            ]
    def __repr__(self):
        return "<{0}[{1}].{2}({3})>".format(
            self.__class__.__name__,
            self._get_kwargs_str(self._get_setup_kwargs()),
            self._testMethodName,
            self._get_kwargs_str(self._get_method_kwargs()),
            )
    def __str__(self):
        return repr(self)
    def _get_kwargs_str(self, kwargs):
        return ', '.join(
            "{0}={1!r}".format(key, value) for key, value in kwargs.iteritems()
            )




