import unittest

from scopeton import compat, scope


class Dependency3(object):
    def test(self):
        print ("test called")
    def testDecorated(self):
        print ("test called")
    def testDecoratedSame(self):
        print("test called")


class CompatTest(unittest.TestCase):

    def test_GetMethodInstance(self):
        instance = Dependency3()
        res = compat.get_method_instance(instance.test)
        self.assertEqual(instance, res)




if __name__ == "__main__":
    unittest.main()
