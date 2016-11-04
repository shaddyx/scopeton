import copy
import os
import sys
import DiTools
from ContextBean import ContextBean
from threading import RLock

class ScopeContext(object):
    def __init__(self, beans):
        # type: (dict[str, ContextBean]) -> object
        self.__instances = {}  # type: dict[str, object]
        self.scopeLock = RLock()
        self.beans = beans

    def resolveClass(self, name):
        # type: (object) -> ContextBean
        pkg = DiTools.getFullyQualifiedName(name)
        if pkg not in self.beans:
            raise Exception("Error, no class with name {pkg} registered, available:{keys}".format(pkg=pkg, keys=self.beans.keys()))
        return self.beans[pkg]

    def makeInstance(self, cls):
        # type: (ContextBean) -> object
        instance = cls.object()
        instance.contextScope = self
        if hasattr(instance, "_inject"):
            instance._inject()
        return instance

    def getInstance(self, obj):
        name = DiTools.getFullyQualifiedName(obj)
        if name in self.__instances:
            return self.__instances[name]
        self.scopeLock.acquire()
        cls = self.resolveClass(obj)
        if name not in self.__instances:
            self.__instances[name] = self.makeInstance(cls)

        self.scopeLock.release()
        return self.__instances[name]


def InjectClass(**kwargs_):
    def decorator(cls):
        def inject(self):
            for name in kwargs_:
                setattr(self, name, self.contextScope.getInstance(kwargs_[name]))
        cls._inject =inject
        return cls
    return decorator
