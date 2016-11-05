import unittest

from dipy.DiTools import getScope
from dipy.ScopeAnnotations import InjectClass
from dipy.ScopeContext import ScopeContext
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


class ScopeContextTest(unittest.TestCase):

    def test_LocatorGetInstance(self):
        context = ScopeContext(StaticContext.getBeansCopy())
        dep1 = context.getInstance(Dependency1)
        dep1_n = context.getInstance(Dependency1)
        self.assertEqual(dep1, dep1_n)

    def test_LocatorGetScope(self):
        context = ScopeContext(StaticContext.getBeansCopy())
        dep1 = context.getInstance(Dependency1)
        self.assertEqual(getScope(dep1), context)

    def testInjectClass(self):
        context = ScopeContext(StaticContext.getBeansCopy())
        dep3 = context.getInstance(Dependency3)
        self.assertTrue(isinstance(dep3.dep1, Dependency1))
        self.assertTrue(isinstance(dep3.dep2, Dependency2))

if __name__ == "__main__":
    unittest.main()
