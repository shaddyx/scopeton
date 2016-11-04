import new
import os
import sys
def getSimpleNameFromString(obj):
    return obj.split(".")[-1]

def getSimpleClassNameFromObject(obj):
    """returns class name (without package for given object)"""
    # type: (object) -> str
    tp = type(obj)
    if tp is new.classobj or tp is type:
        return getSimpleNameFromString(obj.__name__)
    elif tp is str:
        return obj
    elif tp is new.instance:
        return getSimpleNameFromString(obj.__class__.__name__)
    raise Exception("Cannot get className for object:" + str(type(obj)))


def getObjectPackage(obj):
    # type: (object) -> str
    """returns object package"""
    if type(obj) is str:
        return obj
    # mod = sys.modules[obj.__module__]
    # dir = os.path.dirname(mod.__file__)

    # print "modulepath:" + str(obj.__module__)
    # print "path:" + os.path.dirname(sys.argv[0])
    return obj.__module__

def getFullyQualifiedName(obj):
    # type: (object) -> str
    """returns class name with package"""
    result = []
    package = getObjectPackage(obj)
    if package:
        result.append(package)
    result.append(getSimpleClassNameFromObject(obj))
    return ".".join(result)

def getScope(scopeHolder):
    if hasattr(scopeHolder, "__scope"):
        return scopeHolder.__scope
    raise Exception("Error, object is not scopeHolder:" + scopeHolder)
