# try to patch nose's transplant_class
def _patch_nose_transplant_class(module_name):
    try:
        module = __import__(module_name)
    except ImportError:
        return
    for submodule in module_name.split(".")[1:]:
        module = getattr(module, submodule)
    if hasattr(module, 'transplant_class'):
        module.transplant_class = _patch_transplant_class_function(module.transplant_class)

def _patch_transplant_class_function(original):
    def transplant_class(cls, module):
        new_cls = original(cls, module)
        if new_cls is not cls and is_abstract_base_test(cls):
            new_cls = abstract_base_test(new_cls)
        return new_cls
    return transplant_class

_patch_nose_transplant_class('nose.loader')
_patch_nose_transplant_class('nose.util')

def abstract_base_test(cls):
    cls.__is_abstract__ = True
    return cls
def is_abstract_base_test(cls):
    return bool(cls.__dict__.get('__is_abstract__', False))
