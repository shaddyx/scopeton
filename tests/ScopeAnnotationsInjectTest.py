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

class ScopeAnnotationsInjectTest(unittest.TestCase):

    def test_PostConstruct(self):
        context = ScopeContext(StaticContext.getBeansCopy())
        dep1 = context.resolveClass(Dependencyz1)

        #self.assertTrue(dep1 in called)

if __name__ == "__main__":
    unittest.main()
