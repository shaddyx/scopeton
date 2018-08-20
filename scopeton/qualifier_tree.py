import logging
import typing
from threading import RLock

from scopeton.scopeTools import ScopetonException, flatten


class QualifierTree:
    def __init__(self):
        self._qualifiers = {}  # type: dict[str, typing.List[_Wrapper]]
        self.lock = RLock()

    def _registerObj(self, qualifier_name: str, obj, replace):
        with self.lock:
            if replace or (qualifier_name not in self._qualifiers):
                self._qualifiers[qualifier_name] = []
            if obj not in self._qualifiers[qualifier_name]:
                logging.debug("Registering: {}".format(obj))
                self._qualifiers[qualifier_name].append(obj)

    def register(self, names: typing.Union[typing.List[str], str], obj, replace=False):
        if isinstance(names, str):
            names = [names]
        for name in names:
            self._registerObj(name, obj, replace)

    def contains(self, name):
        return name in self._qualifiers

    def get_all_objects(self):
        lists = flatten([self._qualifiers[q] for q in self._qualifiers])
        return list(set(lists))

    def find_by_qualifier_name(self, name):
        with self.lock:
            if name not in self._qualifiers:
                raise ScopetonException("Error, no such qualifier: {}".format(name))
            if len(self._qualifiers[name]) > 1:
                raise ScopetonException("{} qualifier for name: {}, expected 1, objects: {}".format(len(self._qualifiers[name]), name, self._qualifiers[name]))

            return self._qualifiers[name][0]