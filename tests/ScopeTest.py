import unittest

from scopeton import scope
from scopeton.objects import Bean


class Dependency2(object):
    def __init__(self, context):
        self.context = context
        self.dep3 = context.getInstance(Dependency3)

    called = False
    def postConstruct(self):
        print("PostConstruct called")
        self.called = True

    def test(self):
        print ("test called")
    def testDecorated(self):
        print ("test called")
    def testDecoratedSame(self):
        print("test called")

class Dependency3(object):
    def test(self):
        print ("test called")
    def testDecorated(self):
        print ("test called")
    def testDecoratedSame(self):
        print("test called")


class ScopeTest(unittest.TestCase):

    def test_RegisterAndGetInstance(self):
        appScope = scope.Scope()
        appScope.registerBean(Bean(Dependency2), Bean(Dependency3))
        dep2 = appScope.getInstance(Dependency2)  # type: Dependency2
        dep3 = appScope.getInstance(Dependency3)
        dep3_single = appScope.getInstance(Dependency3)
        appScope.runServices()
        self.assertTrue(isinstance(dep3, Dependency3))
        self.assertEqual(dep3, dep3_single)
        self.assertEqual(dep2.dep3, dep3_single)
        self.assertTrue(isinstance(dep2, Dependency2))
        self.assertTrue(dep2.called)

if __name__ == "__main__":
    unittest.main()
