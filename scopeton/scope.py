import logging
from threading import RLock

from scopeton.bean import Bean
from scopeton.scopeTools import getBeanName, callMethodByName


class Scope(object):
    '''this is servicelocator pattern implementation'''
    def __init__(self, lock=False, initMethod="postConstruct", destroyMethod="preDestroy"):
        self._singletons = {}  # type: dict[str, Bean]
        self._beans = {}       # type: dict[str, Bean]
        self.lock = lock       # type: RLock
        self.initMethod = initMethod
        self.destroyMethod = destroyMethod

    def getInstance(self, name):
        if self.lock:
            self.lock.acquire()
        try:
            return self._getInstance(getBeanName(name))
        finally:
            if self.lock: self.lock.release()

    def _getInstance(self, name):
        name = getBeanName(name)
        if name in self._singletons:
            return self._singletons[name]

        if name not in self._beans:
            raise Exception("Error, no such bean:" + str(name))

        bean = self._beans[name]
        instance = bean.cls()
        if bean.singleton:
            self._singletons[name] = instance
        return instance

    def registerBean(self, *args):
        if self.lock:
            self.lock.acquire()
        try:
            for bean in args:
                self._registerBean(bean)
        finally:
            if self.lock: self.lock.release()

    def _registerBean(self, bean):
        """
        :type bean: Bean
        """
        logging.debug("Registering:" + getBeanName(bean))
        self._beans[getBeanName(bean)] = bean

    def runServices(self):
        for k in self._beans:
            bean = self._beans[k]
            if bean.service:
                callMethodByName(self.getInstance(bean), self.initMethod)
