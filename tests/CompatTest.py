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
        compat.getMethodSignature(Dependency3.__init__)



if __name__ == "__main__":
    unittest.main()
