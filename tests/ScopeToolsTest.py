import unittest

from scopeton import scope, scopeTools
from scopeton.scopeTools import callMethodByName, getBean_qualifier


class Cls1(object):
    pass
class Cls2(Cls1, object):
    pass
class Cls3(Cls2, Cls1):
    pass
class Cls4(Cls3):
    pass
class Cls5(Cls4):
    pass

class Dependency2(object):
    called = False
    def test(self):
        print ("test called")
    def testDecorated(self, param):
        print ("test called" + param)
        self.called = param
    def testDecoratedSame(self):
        print("test called")

class ScopeTest(unittest.TestCase):

    def test_GetBeanName(self):
        dep2 = getBean_qualifier(Dependency2)
        self.assertEqual(dep2, 'Dependency2')

    def test_callMethodByname(self):
        dep2 = Dependency2()
        callMethodByName(dep2, "testDecorated", "aaa")
        self.assertEqual(dep2.called, "aaa")

    def test__flatten(self):
        res = scopeTools.flatten([
            [123, 234],
            567,
            [789, [9876, [4324]]]
        ])
        self.assertEqual([123, 234, 567, 789, 9876, 4324], res)

    def test_getClassesTree(self):
        res = scopeTools.getClassTree(Cls5)
        res = [k.__name__ for k in res]
        self.assertEqual(['Cls5', 'Cls4', 'Cls3', 'Cls2', 'Cls1', 'object'] , res)

    def test_getClassesTree(self):
        res = scopeTools.getClassTreeQualifiers(Cls5)
        self.assertEqual(['Cls5', 'Cls4', 'Cls3', 'Cls2', 'Cls1', 'object'] , res)

if __name__ == "__main__":
    unittest.main()
