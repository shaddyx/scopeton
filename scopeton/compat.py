import inspect
import sys

def isPython3():
    return sys.version_info.major >= 3

def get_class_that_defined_method_py3(meth):
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
           if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth), meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if isinstance(cls, type):
            return cls
    return getattr(meth, '__objclass__', None)  # handle special descriptor objects

def get_class_that_defined_method_py2(meth):
    return meth.im_class

def get_class_that_defined_method(meth):
    if isPython3():
        return get_class_that_defined_method_py3(meth)
    else:
        return get_class_that_defined_method_py2(meth)
