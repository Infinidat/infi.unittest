def abstract_base_test(cls):
    cls.__is_abstract__ = True
    return cls
def is_abstract_base_test(cls):
    return bool(cls.__dict__.get('__is_abstract__', False))
