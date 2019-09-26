import inspect
import sys

from scopeton import constants


class _Python2NativeArgs:
    args = ['self']

def isPython3():
    return sys.version_info.major >= 3

def getMethods(instance):
    return [k for k in inspect.getmembers(instance, predicate=inspect.ismethod)]

def isClass(obj):
    if not isPython3():
        import new
        return type(obj) is new.classobj or type(obj) is type
    else:
        import inspect
        return inspect.isclass(obj)

def objectIsInstance(obj):
    if not isPython3():
        import new
        return type(obj) is new.instance or (hasattr(obj, "__class__") and hasattr(obj.__class__, "__name__"))
    else:
        import inspect
        return inspect.isclass(obj)


def getMethodSignature(method):
    if isPython3():
        return inspect.getfullargspec(method)
    else:
        try:
            return inspect.getargspec(method)
        except TypeError:
            return _Python2NativeArgs()


def hasInject(fn):
    return hasattr(fn, constants.INJECT_FLAG)


def isMethod(fn):
    return inspect.ismethod(fn)