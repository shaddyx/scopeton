from threading import RLock

from scopeton import compat
from scopeton.objects import Bean
from scopeton.qualifier_tree import QualifierTree
from scopeton.scopeTools import getBean_qualifier, callMethodByName


class Scope(object):
    '''this is servicelocator pattern implementation'''
    def __init__(self, lock=False, initMethod="postConstruct", destroyMethod="preDestroy", parent=None):
        self._singletons = QualifierTree()
        self._beans = QualifierTree()
        self.lock = lock or RLock()       # type: RLock
        self.initMethod = initMethod
        self.destroyMethod = destroyMethod
        self.parent = parent    #type: Scope

    def getInstance(self, name):
        self.lock.acquire()
        try:
            return self._getInstance(getBean_qualifier(name))
        finally:
            self.lock.release()

    def _getInstance(self, qualifier):

        if self._singletons.contains(qualifier):
            return self._singletons.find_by_qualifier_name(qualifier)

        bean = self._beans.find_by_qualifier_name(qualifier)

        if len(compat.getMethodSignature(bean.cls.__init__).args) == 2:
            instance = bean.cls(self)
        else:
            instance = bean.cls()

        if bean.singleton:
            self.registerInstance(qualifier, instance)

        return instance

    def registerInstance(self, names, instance):
        self._singletons.register(names, instance)

    def registerBean(self, *args):
        self.lock.acquire()
        try:
            for bean in args:
                if not isinstance(bean, Bean):
                    bean = Bean(bean)
                self._registerBean(bean)
        finally:
            self.lock.release()

    def _registerBean(self, bean):
        """
        :type bean: Bean
        """
        for name in bean.qualifier_tree:
            self._beans.register(name, bean)

    def runServices(self):
        for bean in self._beans.get_all_objects():
            if bean.service:
                callMethodByName(self.getInstance(bean), self.initMethod)
