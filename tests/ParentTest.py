import logging
import unittest
from unittest.mock import Mock

from scopeton import scope
from scopeton.decorators import Inject
from scopeton.objects import Bean
from scopeton.scopeTools import ScopetonException

class ParentTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def test_RegisterAndGetInstance(self):
        appScope = scope.Scope()
        childScope = scope.Scope(parent=appScope)
        childScope1 = scope.Scope(parent=appScope)
        appScope.runServices()
        self.assertEqual(2, len(appScope.children))
        appScope.remove()
        self.assertEqual(0, len(appScope.children))
        self.assertFalse(appScope.servicesStarted)


if __name__ == "__main__":
    unittest.main()
