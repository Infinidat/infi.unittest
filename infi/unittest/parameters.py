import logging
import itertools
import functools
from collections import defaultdict
from .python3_compat import items_list
from .call import Call, EMPTY_CALL
from .exceptions import InvalidBaseClassException

def iterate(argument_name, options):
    def _decorator(func):
        spec, created = get_or_create_parameter_specs(func)
        spec.add_range(argument_name, options)
        if created:
            @functools.wraps(func)
            def new_func(self):
                call = _get_spec_call_bindings(self)[spec.id]
                return func(self, *call.args, **call.kwargs)
        else:
            new_func = func
        return new_func
    return _decorator

def _get_spec_call_bindings(obj):
    returned = getattr(obj, "_spec_call_bindings", None)
    if returned is None:
        raise InvalidBaseClassException("{0} does not derive from infi.unittest.TestCase, or did not initialize properly".format(obj))
    return returned

def toggle(*names):
    def _decorator(func):
        for name in names:
            func = iterate(name, [True, False])(func)
        return func
    return _decorator

def get_parameter_spec(function):
    return getattr(function, "__infi_unittest_specs__", NO_SPECS)

def get_or_create_parameter_specs(function):
    returned = get_parameter_spec(function)
    created = False
    if returned is NO_SPECS:
        created = True
        returned = function.__infi_unittest_specs__ = ParameterSpecs()
    return returned, created

NO_SPEC_ID = None

class _NO_SPECS(object):
    id = NO_SPEC_ID
    def iterate_calls(self):
        return [EMPTY_CALL]

NO_SPECS = _NO_SPECS()

_id_counter = itertools.count()

class ParameterSpecs(object):
    def __init__(self):
        super(ParameterSpecs, self).__init__()
        self._params = defaultdict(OptionList)
        self.id = next(_id_counter)
    def add_range(self, name, options):
        self._params[name].add_range(options)
    def iterate_calls(self):
        items = items_list(self._params)
        for kwargs in self._iterate_kwargs(items):
            call = Call(**kwargs)
            logging.debug("Yielding %s", call)
            yield call
    def _iterate_kwargs(self, args_and_options):
        if not args_and_options:
            return
        if len(args_and_options) == 1:
            for option in args_and_options[0][1]:
                yield {args_and_options[0][0]:option}
        else:
            arg_name, options = args_and_options[0]
            for option in options:
                for kwargs in self._iterate_kwargs(args_and_options[1:]):
                    kwargs[arg_name] = option
                    yield kwargs

class OptionList(object):
    def __init__(self):
        super(OptionList, self).__init__()
        self._ranges = []
    def add_range(self, range):
        self._ranges.append(range)
    def __iter__(self):
        for option_list in self._ranges:
            if hasattr(option_list, "__call__"):
                option_list = option_list()
            for option in option_list:
                yield option
    def __repr__(self):
        return "[{0}]".format(", ".join(map(repr, self._get_repr_items())))
    def _get_repr_items(self):
        for option_list in self._ranges:
            if hasattr(option_list, "__call__"):
                yield option_list
            else:
                for x in option_list:
                    yield x
