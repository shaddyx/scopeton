import unittest

from scopeton.qualifier_tree import QualifierTree
from scopeton.scope_tools import ScopetonException


class ScopeTest(unittest.TestCase):

    def test_register(self):
        tree = QualifierTree()
        tree.register("aaa", 1)
        tree.register("bbb", 2)
        tree.register(["zzz", "bbb", "ccc"], 3)
        res = tree.find_one_by_qualifier_name("aaa")
        self.assertEqual(1, res)
        self.assertEqual(3, tree.find_one_by_qualifier_name("zzz"))
        self.assertEqual(3, tree.find_one_by_qualifier_name("ccc"))

    def test_register_multiple(self):
        tree = QualifierTree()
        tree.register(["aaa", "bbb", "ccc"], 1)
        tree.register(["aaa", "bbb", "ddd"], 2)
        self.assertEqual(1, tree.find_one_by_qualifier_name("ccc"))
        self.assertEqual(2, tree.find_one_by_qualifier_name("ddd"))

    def test_error(self):
        tree = QualifierTree()
        tree.register(["aaa", "bbb", "ddd"], 1)
        tree.register(["aaa", "bbb", "ddd"], 2)
        try:
            self.assertEqual(2, tree.find_one_by_qualifier_name("ddd"))
            ok = False
        except ScopetonException:
            ok = True

        self.assertTrue(ok)

    def test_get_object(self):
        tree = QualifierTree()
        tree.register(["aaa", "bbb", "ddd"], 1)
        tree.register(["aaa", "bbb", "ddd"], 2)
        res = sorted(tree.get_all_objects())
        self.assertEqual([1, 2], res)

    def test_find_qualifiers(self):
        tree = QualifierTree()
        tree.register(["aaa", "bbb", "ccc", "eee"], 1)
        tree.register(["aaa", "bbb", "ddd"], 2)
        res = tree.find_qualifiers(1)
        self.assertEqual(["aaa", "bbb", "ccc", "eee"], res)

    def test_find_suitable_qualifier(self):
        tree = QualifierTree()
        tree.register(["aaa", "bbb", "ccc", "eee", "zzz", "kkkk"], 1)
        tree.register("aaa", 1)
        tree.register(["aaa", "bbb", "ddd", "yyy", "rrr", "zzz", "kkk"], 2)
        res = tree.find_suitable_qualifier("eee")
        self.assertEqual("kkkk", res)
        res = tree.find_suitable_qualifier("rrr")
        self.assertEqual("kkk", res)


if __name__ == "__main__":
    unittest.main()
