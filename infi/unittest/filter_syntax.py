import re

_ARGS = r"\[[^]]+\]"

_IDENTITIFER = r"[a-zA-Z_][_0-9a-zA-Z]*"
_MODULE_PATH = r"[\.a-zA-Z_][\._0-9a-zA-Z]*"

def _REMEMBER(x, name):
    return "(?P<{0}>{1})".format(name, x)

def _OPTIONAL(*x):
    return "(?:{0})?".format(''.join(x))


FILTER_STRING_RE = ''.join((
    '^',
    _REMEMBER(_MODULE_PATH, "module_name"),
    _OPTIONAL(
        ":",
        _REMEMBER(_IDENTITIFER, "class_name"),
        _OPTIONAL(
            _REMEMBER(_ARGS, "setup_call")
            ),
        _OPTIONAL(
            ".",
            _REMEMBER(_IDENTITIFER, "method_name"),
            _OPTIONAL(
                _REMEMBER(_ARGS, "method_call")
                )
            )
        ),
    '$'
    ))

FILTER_STRING_PATTERN = re.compile(FILTER_STRING_RE)
