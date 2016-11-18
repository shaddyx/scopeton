import unittest

from scopeton import DiTools
from scopeton.ScopeAnnotations import PostConstruct, PreDestroy
from scopeton.StaticContext import Service
from package1.testPackageClass import PackageClass

@Service()
class DependencyWithSingleMethod(object):
    def firstMethod(self):
        pass

@Service()
class Dependency1(object):
    pass
@Service()
class Dependency2(object):

    @PostConstruct()
    def method1(self):
        pass

    def method2(self):
        pass


class DIToolsTest(unittest.TestCase):

    def testGetSimpleNameFromString(self):
        self.assertEqual("TestClass", DiTools.getSimpleNameFromString("ua.org.shaddy.TestClass"))

    def testGetSimpleClassNameFromObject(self):
        self.assertEqual("Dependency1", DiTools.getSimpleClassNameFromObject(Dependency1))

    def testGetObjectPackage(self):
        self.assertEqual("package1.testPackageClass", DiTools.getObjectPackage(PackageClass))

    def testGetFullyQualifiedName(self):
        self.assertEqual("package1.testPackageClass.PackageClass", DiTools.getFullyQualifiedName(PackageClass))

    def testGetClassMethods(self):
        self.assertEqual(DiTools.getClassMethods(DependencyWithSingleMethod)[0], DependencyWithSingleMethod.firstMethod)

    def testGetAnnotatedMethods(self):
        self.assertTrue(Dependency2.method1 in DiTools.getBeanMethodsInitializers(Dependency2))


if __name__ == "__main__":
    unittest.main()
