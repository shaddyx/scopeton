import logging
import unittest

from scopeton import scope
from scopeton.decorators import Inject
from scopeton.scope_tools import ScopetonException


class Dependency1:
    pass


class Dependency8:
    called = False

    @Inject()
    def inject_method(self, dep1: Dependency1):
        self.called = True
        assert isinstance(dep1, Dependency1)


class ScopeTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def test_RegisterAndGetInstanceInjectorOnSomeMethod(self):
        app_scope = scope.Scope()
        app_scope.registerBean(Dependency1, Dependency8)
        instance = app_scope.getInstance(Dependency8)
        self.assertTrue(instance.called, "Injector is not called!")

if __name__ == "__main__":
    unittest.main()
