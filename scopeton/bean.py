from scopeton.scopeTools import getBeanName


class Bean(object):
    name = ""
    cls = None  # type: type
    lazy = False
    singleton = True

    def __init__(self, cls, name=None, lazy = False, singleton=True):
        self.cls = cls
        self.name = name or getBeanName(cls)
        self.lazy = lazy
        self.singleton = singleton



