import unittest

from scopeton.ScopeAnnotations import PostConstruct
from scopeton.ScopeContext import ScopeContext
from scopeton.StaticContext import Service, StaticContext

called = []
@Service()
class Dependencyz1(object):

    @PostConstruct()
    def init(self):
        called.append(self)


@Service()
class Dependencyz2(object):

    @PostConstruct()
    def init(self):
        called.append(self)
class ScopeAnnotationsTest(unittest.TestCase):

    def test_PostConstruct(self):
        context = ScopeContext(StaticContext.getBeansCopy())
        print ("OK")
        dep1 = context.getInstance(Dependencyz1)
        self.assertTrue(dep1 in called)
        dep1_n = context.getInstance(Dependencyz2)
        self.assertTrue(dep1_n in called)
        self.assertTrue(dep1 in called)

if __name__ == "__main__":
    unittest.main()
