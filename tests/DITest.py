import unittest

from dipy.DI import InjectClass, ScopeContext
from dipy.StaticContext import Service, StaticContext


@Service()
class Dependency1(object):
    pass
@Service()
class Dependency2(object):
    pass

@InjectClass(dep2=Dependency2, dep1=Dependency1)
@Service()
class Dependency3(object):
    def __init__(self):
        print "constructor3 called"


class FileToolsTest(unittest.TestCase):

    def test_LocatorGetInstance(self):
        context = ScopeContext(StaticContext.getBeansCopy())
        dep1 = context.getInstance(Dependency1)
        dep1_n = context.getInstance(Dependency1)
        self.assertEqual(dep1, dep1_n)

    def test_LocatorGetInstance(self):
        context = ScopeContext(StaticContext.getBeansCopy())
        dep1 = context.getInstance(Dependency1)
        dep1_n = context.getInstance(Dependency2)
        self.assertNotEqual(dep1, dep1_n)

    def testInjectClass(self):
        context = ScopeContext(StaticContext.getBeansCopy())
        dep3 = context.getInstance(Dependency3)
        self.assertTrue(isinstance(dep3.dep1, Dependency1))
        self.assertTrue(isinstance(dep3.dep2, Dependency2))

if __name__ == "__main__":
    unittest.main()
