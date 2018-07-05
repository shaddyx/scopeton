import unittest

from scopeton import compat


class Dependency3(object):
    def test(self):
        print ("test called")
    def testDecorated(self):
        print ("test called")
    def testDecoratedSame(self):
        print("test called")


class CompatTest(unittest.TestCase):

    def test_GetMethodClass(self):
        pass
        #res = compat.getMethodClass(Dependency3.test)
        #self.assertEqual(res, Dependency3)


if __name__ == "__main__":
    unittest.main()
