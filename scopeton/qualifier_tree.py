import typing
from threading import RLock

from scopeton.scopeTools import ScopetonException, flatten


class _Wrapper:
    def __init__(self, current_name, qualifier_names: typing.List[str], object):
        self.qualifier_names = qualifier_names
        self.object = object
        self.current_name = current_name

class QualifierTree:
    def __init__(self):
        self._qualifiers = {}  # type: dict[str, typing.List[_Wrapper]]
        self.lock = RLock()

    def _register(self, qualifier_name: str, wrapper: _Wrapper):
        self.lock.acquire()
        try:
            if qualifier_name not in self._qualifiers:
                self._qualifiers[qualifier_name] = []
            self._qualifiers[qualifier_name].append(wrapper)
        finally:
            self.lock.release()

    def register(self, names: typing.Union[typing.List[str], str], obj):
        if isinstance(names, str):
            names = [names]
        for name in names:
            self._register(name, _Wrapper(name, names, obj))

    def contains(self, name):
        return name in self._qualifiers

    def get_all_objects(self):
        lists = flatten([self._qualifiers[q] for q in self._qualifiers])
        return list(set([q.object for q in lists]))

    def find_by_qualifier_name(self, name):
        self.lock.acquire()
        try:
            if name not in self._qualifiers:
                raise ScopetonException("Error, no such qualifier: {}".format(name))
            if len(self._qualifiers[name]) > 1:
                raise ScopetonException("{} qualifier for name: {}, expected 1, objects: {}".format(len(self._qualifiers[name]), name, self._qualifiers[name]))

            return self._qualifiers[name][0].object
        finally:
            self.lock.release()
