import logging
import unittest

from scopeton import scope
from scopeton.decorators import Inject
from scopeton.objects import Bean


class Dependency1(object):
    received_instance = None

    @Inject()
    def _injector(self, a: "test_instance"):
        assert isinstance(a, int)
        assert a == 1
        self.received_instance = a

    pass


class Dependency2(object):
    pass


class Dependency3(object):
    pass


class ScopeStringTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def test_RegisterAndGetInstance(self):
        appScope = scope.Scope()
        appScope.registerBean(Bean(Dependency2), Bean(Dependency3))
        dep2 = appScope.getInstance("Dependency2")  # type: Dependency2
        assert isinstance(dep2, Dependency2)

    def test_registerIntInstanceAndGetInstance(self):
        appScope = scope.Scope()
        appScope.registerInstance("test_instance", 1)
        appScope.registerInstance("test_instance1", 2)
        assert appScope.getInstance("test_instance") == 1
        assert appScope.getInstance("test_instance1") == 2

    def test_registerIntInstanceAndInject(self):
        appScope = scope.Scope()
        appScope.registerBean(Bean(Dependency1))
        appScope.registerInstance("test_instance", 1)
        instance = appScope.getInstance(Dependency1)
        assert instance.received_instance == 1


if __name__ == "__main__":
    unittest.main()
