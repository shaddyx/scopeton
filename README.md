# Scopeton

Scopeton is a simple dependency injection framework for Python inspired by the Java Spring framework

Main entities of the scopeton:

* Scope - the context of the application
* Bean - the small brick of the application to inject, can be singleton (default) or multiton

## Installation

```pip install scopeton```

## Basic usage

Firstly you have to create a scope and register beans there:

```python
from scopeton import scope
class Dependency1:
    pass
class Dependency2:
    pass
class Dependency3:
    pass
appScope = scope.Scope()
appScope.registerBean(Dependency1, Dependency2, Dependency3)
```

There are several ways how to get the instance of dependency from the scope:
1. Service locator style: 
```python
    depencency1Instance = appScope.getInstance(Dependency1) - returns the singleton instance of Dependency1  
```
2. Automatic constructor injection:
```python
from scopeton import scope
from scopeton.decorators import Inject
from scopeton.scopeTools import ScopetonException

class Dependency1():
    pass

class Dependency4():
    pass

class Dependency5():
    @Inject()
    def __init__(self, dep1: Dependency1, a):
        pass


class Dependency7():
    called = False
    @Inject()
    def __init__(self, dep1:Dependency1, dep4: Dependency4):
        assert isinstance(dep1, Dependency1)
        assert isinstance(dep4, Dependency4)
        
appScope = scope.Scope()
appScope.registerBean(Dependency1, Dependency4, Dependency5, Dependency7)
instance = appScope.getInstance(Dependency7)

```
in this case the Dependency1 and Dependency4 will be injected automatically to the constructor of the Dependency7
