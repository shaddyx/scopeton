import unittest

from microtools.DI import Service

from dipy.DiTools import getSimpleNameFromString, getObjectPackage, getSimpleClassNameFromObject, getFullyQualifiedName
from package1.testPackageClass import PackageClass


@Service()
class Dependency1(object):
    pass
@Service()
class Dependency2(object):
    pass

class DIToolsTest(unittest.TestCase):

    def testGetSimpleNameFromString(self):
        self.assertEqual("TestClass", getSimpleNameFromString("ua.org.shaddy.TestClass"))

    def testGetSimpleClassNameFromObject(self):
        self.assertEqual("Dependency1", getSimpleClassNameFromObject(Dependency1))

    def testGetObjectPackage(self):
        self.assertEqual("package1.testPackageClass", getObjectPackage(PackageClass))

    def testGetFullyQualifiedName(self):
        self.assertEqual("package1.testPackageClass.PackageClass", getFullyQualifiedName(PackageClass))



if __name__ == "__main__":
    unittest.main()
