import itertools
from .python3_compat import iteritems

class Call(object):
    def __init__(self, *args, **kwargs):
        super(Call, self).__init__()
        self._key = (args, kwargs)
        self.args = args
        self.kwargs = kwargs
    def __eq__(self, other):
        return type(self) is type(other) and self._key == other._key
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        raise TypeError("Call objects are unhashable")
    def __repr__(self):
        args_item_strs = map(repr, self.args)
        kwargs_item_strs = ("{0}={1!r}".format(key, value) for key, value in iteritems(self.kwargs))
        return "({0})".format(", ".join(itertools.chain(args_item_strs, kwargs_item_strs)))
    def __nonzero__(self):
        return bool(self.args) or bool(self.kwargs)

EMPTY_CALL = Call()
