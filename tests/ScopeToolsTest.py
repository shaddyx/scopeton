import unittest

from scopeton import scope
from scopeton.objects import Bean
from scopeton.scopeTools import getBeanName, callMethodByName


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
        dep2 = getBeanName(Dependency2)
        self.assertEqual(dep2, 'Dependency2')

    def test_callMethodByname(self):
        dep2 = Dependency2()
        callMethodByName(dep2, "testDecorated", "aaa")
        self.assertEqual(dep2.called, "aaa")


if __name__ == "__main__":
    unittest.main()
