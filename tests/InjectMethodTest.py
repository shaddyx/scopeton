import logging
import unittest

from scopeton import scope
from scopeton.decorators import Inject
from scopeton.scopeTools import ScopetonException


class Dependency1:
    pass


class Dependency4:
    pass


class Dependency5:
    @Inject()
    def __init__(self, dep1: Dependency1, a):
        pass


class Dependency7:
    called = False

    @Inject()
    def __init__(self, dep1: Dependency1, dep4: Dependency4):
        assert isinstance(dep1, Dependency1)
        assert isinstance(dep4, Dependency4)
        self.called = True


class Dependency8:
    called = False

    @Inject()
    def inject_method(self, dep1: Dependency1):
        self.called = True
        assert isinstance(dep1, Dependency1)


class ScopeTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def test_RegisterAndGetInstance(self):
        app_scope = scope.Scope()
        app_scope.registerBean(Dependency1, Dependency4, Dependency5, Dependency7)
        instance = app_scope.getInstance(Dependency7)
        self.assertTrue(instance.called, "Constructor is not called!")

    def test_RegisterAndGetInstanceInjectorOnSomeMethod(self):
        app_scope = scope.Scope()
        app_scope.registerBean(Dependency1, Dependency8)
        instance = app_scope.getInstance(Dependency8)
        self.assertTrue(instance.called, "Injector is not called!")

    def test_RegisterAndGetInstanceError(self):
        app_scope = scope.Scope()
        app_scope.registerBean(Dependency1, Dependency4, Dependency5, Dependency7)
        try:
            instance = app_scope.getInstance(Dependency5)
            self.fail("Exception expected")
        except ScopetonException as e:
            pass


if __name__ == "__main__":
    unittest.main()
