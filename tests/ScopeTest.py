import unittest
from unittest.mock import Mock

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

class Dependency4(object):
    pass

class Dependency5(Dependency4):
    pass

class Dependency6(Dependency4):
    pass

class Dependency7(Dependency4, Dependency3):
    pass

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


    def test_RegisterAndGetInstanceCustomNames(self):
        appScope = scope.Scope()
        appScope.registerBean(Bean(Dependency4, name=Dependency3), Bean(Dependency4, name="aaa"))

        dep2 = appScope.getInstance(Dependency3)  # type: Dependency4
        dep3 = appScope.getInstance("aaa")
        self.assertNotEqual(dep2, dep3)
        self.assertEqual(dep2.__class__, dep3.__class__)

    def test_same(self):
        appScope = scope.Scope()
        appScope.registerBean(
            Bean(Dependency7),
            Bean(Dependency7)
        )
        appScope.getInstance(Dependency7)


    def test_register_instance(self):
        appScope = scope.Scope()
        appScope.registerBean(
            Bean(Dependency7)
        )
        a = appScope.getInstance(Dependency7)
        b = appScope.getInstance(Dependency4)
        self.assertEqual(a, b)


    def test_mock(self):
        appScope = scope.Scope()
        appScope.registerBean(
            Bean(Mock(Dependency7), name=Dependency7)
        )

        appScope = scope.Scope()
        appScope.registerInstance(
            Dependency7, Mock(Dependency7)
        )

    def test_Inheritance(self):
        appScope = scope.Scope()
        appScope.registerBean(
            Bean(Dependency7)
        )
        dep3 = appScope.getInstance(Dependency4)
        self.assertTrue(dep3, Dependency7)

    def test_Inheritance_multi(self):
        appScope = scope.Scope()
        appScope.registerBean(
            Bean(Dependency5),
            Bean(Dependency7)
        )
        dep3 = appScope.getInstance(Dependency3)
        self.assertTrue(dep3, Dependency7)

        dep4 = appScope.getInstance(Dependency5)
        self.assertTrue(dep3, Dependency7)

    def test_Inheritance_err(self):
        appScope = scope.Scope()
        appScope.registerBean(
            Bean(Dependency5),
            Bean(Dependency7)
        )
        try:
            dep4 = appScope.getInstance(Dependency4)
            ok = False
        except:
            ok=True
        self.assertTrue(ok)


if __name__ == "__main__":
    unittest.main()
