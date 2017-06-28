import unittest

from scopeton.DiTools import getScope
from scopeton.ScopeAnnotations import InjectClass, PostConstruct
from scopeton.ScopeContext import ScopeContext
from scopeton.StaticContext import Service, StaticContext


@Service()
class Dependency1(object):
    pass
@Service()
class Dependency2(object):
    pass

@InjectClass(dep2=Dependency2, dep1=Dependency1, dep3="TestQualifier")
@Service()
class Dependency3(object):
    def __init__(self):
        print ("constructor3 called")

startedImmediatelly = 0
@Service(lazy=False)
class DependStartImmadiatelly(object):
    @PostConstruct()
    def init(self):
        global startedImmediatelly
        startedImmediatelly += 1
        print ("started immediatelly")

@Service(lazy=True)
class DependNotStartImmadiatelly(object):
    @PostConstruct()
    def init(self):
        raise Exception("Need not to start immediatelly")

class DependNotStartImmadiatelly_overload(object):
    @PostConstruct()
    def init(self):
        print ("Overloading ok")

@Service(name="TestQualifier")
class TestQualifierTest(object):
    pass


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
        self.assertTrue(isinstance(dep3.dep3, TestQualifierTest))


    def testStartImmediatelly(self):
        context = ScopeContext(StaticContext.getBeansCopy())
        self.assertNotEqual(0, startedImmediatelly)

    def testStartImmediatelly(self):
        oldStarted = startedImmediatelly
        context = ScopeContext(StaticContext.getBeansCopy(), servicesAutoStart=False)
        self.assertEqual(oldStarted, startedImmediatelly)

    def testRegisterInstance(self):
        context = ScopeContext(StaticContext.getBeansCopy(), servicesAutoStart=False)
        instance = DependNotStartImmadiatelly_overload()
        context.registerInstance(DependNotStartImmadiatelly, instance)
        self.assertEqual(context.getInstance(DependNotStartImmadiatelly), instance)


    def testRegisterBean(self):
        context = ScopeContext(StaticContext.getBeansCopy(), servicesAutoStart=False)
        context.registerBean(DependNotStartImmadiatelly, DependNotStartImmadiatelly_overload)
        self.assertTrue(isinstance(context.getInstance(DependNotStartImmadiatelly), DependNotStartImmadiatelly_overload))



if __name__ == "__main__":
    unittest.main()
