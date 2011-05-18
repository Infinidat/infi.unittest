def iterate(argument_name, options):
    def _decorator(func):
        get_or_create_parameter_specs(func).add_range(argument_name, options)
        return func
    return _decorator

def get_parameter_spec(function):
    return getattr(function, "__infi_unittest_specs__", NO_SPECS)

def get_or_create_parameter_specs(function):
    returned = get_parameter_spec(function)
    if returned is NO_SPECS:
        returned = function.__infi_unittest_specs__ = ParameterSpecs()
    return returned

class _NO_SPECS(object):
    def iterate_args_kwargs(self):
        return [((), {})]
NO_SPECS = _NO_SPECS()

class ParameterSpecs(object):
    def __init__(self):
        super(ParameterSpecs, self).__init__()
        self._params = {}
    def add_range(self, name, options):
        self._params.setdefault(name, []).extend(options)
    def iterate_args_kwargs(self):
        items = list(self._params.iteritems())
        return self._iterate_args_kwargs(items)
    def _iterate_args_kwargs(self, args_and_options):
        if not args_and_options:
            return
        if len(args_and_options) == 1:
            for option in args_and_options[0][1]:
                yield (), {args_and_options[0][0]:option}
        else:
            arg_name, options = args_and_options[0]
            for option in options:
                for args, kwargs in self._iterate_args_kwargs(args_and_options[1:]):
                    kwargs[arg_name] = option
                    yield args, kwargs
