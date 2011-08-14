import itertools
import functools

def iterate(argument_name, options):
    def _decorator(func):
        spec, created = get_or_create_parameter_specs(func)
        spec.add_range(argument_name, options)
        if created:
            @functools.wraps(func)
            def new_func(self):
                params = self._get_parameter_binding(spec.id)
                return func(self, **params)
        else:
            new_func = func
        return new_func
    return _decorator

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
    def iterate_kwargs(self):
        return [{}]
NO_SPECS = _NO_SPECS()


_id_counter = itertools.count()

class ParameterSpecs(object):
    def __init__(self):
        super(ParameterSpecs, self).__init__()
        self._params = {}
        self.id = next(_id_counter)
    def add_range(self, name, options):
        self._params.setdefault(name, []).extend(options)
    def iterate_kwargs(self):
        items = list(self._params.iteritems())
        return self._iterate_kwargs(items)
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
