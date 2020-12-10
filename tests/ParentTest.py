import logging
import unittest

from scopeton import scope


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
