import inspect

from threading import RLock
import sys
from scopeton.ContextBean import ContextBean

cacheLock = RLock()
def getSimpleNameFromString(obj):
    return obj.split(".")[-1]

def isPython3():
    return sys.version_info.major > 2

def getMethodKey(method):
    return method.__name__

def isClass(obj):
    if not isPython3():
        import new
        return type(obj) is new.classobj or type(obj) is type
    else:
        import inspect
        return inspect.isclass(obj)

def isinstance(obj):
    if not isPython3():
        import new
        return type(obj) is new.instance or (hasattr(obj, "__class__") and hasattr(obj.__class__, "__name__"))
    else:
        import inspect
        return inspect.isclass(obj)

def getMethodClass(meth):
    if not hasattr(meth, "__self__"):
        if isPython3():
            method_name = meth.__name__
            if meth.__self__:
                classes = [meth.__self__.__class__]
            else:
                # unbound method
                classes = [meth.im_class]
            while classes:
                c = classes.pop()
                if method_name in c.__dict__:
                    return c
                else:
                    classes = list(c.__bases__) + classes
        else:
            for cls in inspect.getmro(meth.im_class):
                if meth.__name__ in cls.__dict__:
                    return cls
    return meth.__self__.__class__


def __getSimpleClassNameFromObjectInner(obj):
    """returns class name (without package for given object)"""
    # type: (object) -> str
    tp = type(obj)
    if isClass(tp):
        return getSimpleNameFromString(obj.__name__)
    elif tp is str:
        return obj
    elif isinstance(obj):
        return getSimpleNameFromString(obj.__class__.__name__)
    raise Exception("Cannot get className for object:" + str(type(obj)))


def getSimpleClassNameFromObject(obj):
    """returns class name (without package for given object)"""
    # type: (object) -> str
    cacheLock.acquire()
    try:
        if not hasattr(obj, "__simpleClassName"):
            obj.__simpleClassName = __getSimpleClassNameFromObjectInner(obj)
    finally:
        cacheLock.release()
    return obj.__simpleClassName



def getObjectPackage(obj):
    # type: (object) -> str
    """returns object package"""
    if type(obj) is str:
        return obj
    if not hasattr(obj, "__module__"):
        if type(obj).__name__ == 'module':
            possibleError = "Type to inject is module, mb you imported/injected module instead of class: {obj}".format(obj=obj)
        else:
            possibleError = "unknown"

        raise Exception("Error, object has no attribute __module__:{obj}, type:{type}, possible error:{possibleError}".format(obj=obj, type=type(obj), possibleError = possibleError))
    return obj.__module__


def __getFullyQualifiedNameInner(obj):
    # type: (object) -> str
    """returns class name with package"""
    result = []
    package = getObjectPackage(obj)
    if package:
        result.append(package)
    result.append(getSimpleClassNameFromObject(obj))
    return ".".join(result)

def getFullyQualifiedName(obj):
    # type: (object) -> str
    """returns class name with package"""
    if type(obj) is str:
        return obj
    cacheLock.acquire()
    try:
        if not hasattr(obj, "__fullyQualifiedClassName"):
            obj.__fullyQualifiedClassName = __getFullyQualifiedNameInner(obj)
    finally:
        cacheLock.release()
    return obj.__fullyQualifiedClassName

def getScope(scopeHolder):
    if hasattr(scopeHolder, "TTTcontextScope"):
        return scopeHolder.TTTcontextScope
    raise Exception("Error, object is not scopeHolder:" + (str(scopeHolder)))

def getClassMethods(cls):
    # type: (object) -> list[object]
    return list(map(lambda meth: meth[1], inspect.getmembers(cls, predicate=inspect.ismethod)))

def getMethodAnnotations(method):
    clz = getMethodClass(method)
    cacheLock.acquire()
    try:
        if not hasattr(clz, "TTTannotations"):
            clz.TTTannotations = {}
        if method not in clz.TTTannotations:
            clz.TTTannotations[getMethodKey(method)] = []
            return clz.TTTannotations[getMethodKey(method)]
    finally:
        cacheLock.release()

def beanAnnotateMethod(method, annotation):
    cacheLock.acquire()
    annotations = getMethodAnnotations(method)
    try:
        if annotation in annotations:
            raise Exception("Error, method: {methodName} already has annotation: {annotationName}".format(methodName=method.__name__,annotationName=annotation.__name__))
        annotations[method].append(annotation)
    finally:
        cacheLock.release()

def getBeanMethodsInitializers(clazz):
    # type: (object) -> dict[object, object]
    cacheLock.acquire()
    try:
        if hasattr(clazz, "__annotatedMethods"):
            return clazz.__annotatedMethods
        methods = {}
        for method in getClassMethods(clazz):
            if hasattr(clazz, "TTTannotations"):
                methods[method] = clazz.TTTannotations[getMethodKey(method)]
        clazz.__annotatedMethods = methods
        return methods
    finally:
        cacheLock.release()

def createBean(clazz, lazy=True):
    bean = ContextBean()
    bean.lazy = lazy
    bean.name = getFullyQualifiedName(clazz)
    bean.object = clazz
    return bean