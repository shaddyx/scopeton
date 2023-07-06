import unittest

from scopeton import scope, scope_tools
from scopeton.decorators import Inject
from scopeton.scope_tools import call_method_by_name, get_bean_qualifier


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
class InjectableTestClass(object):

    @Inject()
    def test_inhectable_method(self):
        pass

    def test_non_injectable(self):
        pass

class ScopeTest(unittest.TestCase):

    def test_GetBeanName(self):
        dep2 = get_bean_qualifier(Dependency2)
        self.assertEqual(dep2, 'Dependency2')

    def test_callMethodByname(self):
        dep2 = Dependency2()
        call_method_by_name(dep2, "testDecorated", "aaa")
        self.assertEqual(dep2.called, "aaa")

    def test__flatten(self):
        res = scope_tools.flatten([
            [123, 234],
            567,
            [789, [9876, [4324]]]
        ])
        self.assertEqual([123, 234, 567, 789, 9876, 4324], res)

    def test_getClassesTree(self):
        res = scopeTools.get_class_tree(Cls5)
        res = [k.__name__ for k in res]
        self.assertEqual(['object', 'Cls1', 'Cls2', 'Cls3', 'Cls4', 'Cls5'] , res)

    def test_getClassesTree(self):
        res = scope_tools.get_class_tree_qualifiers(Cls5)
        self.assertEqual(['object', 'Cls1', 'Cls2', 'Cls3', 'Cls4', 'Cls5'] , res)

    def test_get_injectables(self):
        res = scope_tools.get_injectables(InjectableTestClass())
        self.assertEqual(1, len(res))


if __name__ == "__main__":
    unittest.main()
