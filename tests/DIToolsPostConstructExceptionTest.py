import unittest

from scopeton.ScopeContext import ScopeContext

from scopeton import DiTools
from scopeton.ScopeAnnotations import PostConstruct, PreDestroy, InjectClass
from scopeton.StaticContext import Service, StaticContext
from package1.testPackageClass import PackageClass

@Service()
class DependencyWithException(object):

    @PostConstruct()
    def method1(self):
        raise Exception("test exception")

@Service()
@InjectClass(dep=DependencyWithException)
class Dependency(object):
    def method2(self):
        pass


class DIToolsPostConstructTest(unittest.TestCase):

    def test_ExceptionInDep(self):
        context = ScopeContext(StaticContext.getBeansCopy())
        try:
            dep3 = context.getInstance(Dependency)
            raise Exception("Error, exception is not thrown")
        except Exception as e:
            self.assertTrue("test exception" in str(e))
            self.assertTrue("DIToolsPostConstructExceptionTest.py" in str(e))
            #print e


if __name__ == "__main__":
    unittest.main()
