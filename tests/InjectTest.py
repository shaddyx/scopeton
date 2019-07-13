import logging
import unittest
from unittest.mock import Mock

from scopeton import scope
from scopeton.decorators import Inject
from scopeton.objects import Bean
from scopeton.scopeTools import ScopetonException


class Dependency1():
    pass

class Dependency4():
    pass

class Dependency5():
    @Inject()
    def __init__(self, dep1: Dependency1, a):
        pass


class Dependency7():
    called = False
    @Inject()
    def __init__(self, dep1:Dependency1, dep4: Dependency4):
        assert isinstance(dep1, Dependency1)
        assert isinstance(dep4, Dependency4)
        self.called = True




class ScopeTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def test_RegisterAndGetInstance(self):
        appScope = scope.Scope()
        appScope.registerBean(Dependency1, Dependency4, Dependency5, Dependency7)
        instance = appScope.getInstance(Dependency7)
        self.assertTrue(instance.called, "Constructor is not called!")

    def test_RegisterAndGetInstanceError(self):
        appScope = scope.Scope()
        appScope.registerBean(Dependency1, Dependency4, Dependency5, Dependency7)
        try:
            instance = appScope.getInstance(Dependency5)
            self.fail("Exception expected")
        except ScopetonException as e:
            pass


if __name__ == "__main__":
    unittest.main()
