import logging
import typing
from threading import RLock

from scopeton.scopeTools import ScopetonException, flatten


class _Wrapper:
    def __init__(self, qualifier_names: typing.List[str], object):
        self.qualifier_names = qualifier_names
        self.object = object
    def __hash__(self):
        self.qualifier_names.__hash__() + self.object.__hash__()
    def __str__(self):
        return "{self.qualifier_names[0]}[{self.object}]".format(self=self)
    def __repr__(self):
        return str(self)

class QualifierTree:
    def __init__(self):
        self._qualifiers = {}  # type: dict[str, typing.List[_Wrapper]]
        self.lock = RLock()

    def _register(self, qualifier_name: str, wrapper: _Wrapper):
        self.lock.acquire()
        try:
            if qualifier_name not in self._qualifiers:
                self._qualifiers[qualifier_name] = []
            if wrapper not in self._qualifiers[qualifier_name]:
                logging.debug("Registering: {}".format(wrapper))
                self._qualifiers[qualifier_name].append(wrapper)
        finally:
            self.lock.release()

    def register(self, names: typing.Union[typing.List[str], str], obj):
        if isinstance(names, str):
            names = [names]
        for name in names:
            self._register(name, _Wrapper(names, obj))

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
