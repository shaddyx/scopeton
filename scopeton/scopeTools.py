def flatten(lst):
    res = []
    for el in lst:
        if type(el) is list:
            res += flatten(el)
        else:
            res.append(el)
    return res

def getClassTreeQualifiers(cls):
    return [getBean_qualifier(k.__name__) for k in getClassTree(cls)]


def rmDups(lst):
    res = []
    for k in lst:
        if k not in res:
            res.append(k)
    return res


def getClassTree(cls):
    return rmDups(_getClassTree(cls))

def _getClassTree(cls):
    res = [cls]
    if type(cls) is not object and hasattr(cls, "__bases__") and cls.__bases__:
        res += flatten([_getClassTree(parent) for parent in cls.__bases__])
    return res

def getBean_qualifier(bean):
    if isinstance(bean, str):
        return bean
    from scopeton.objects import Bean
    if isinstance(bean, Bean):
        return bean.qualifier_tree[0]
    return bean.__name__

def callMethodByName(obj, name, *args, **kwargs):
    if hasattr(obj, name):
        return getattr(obj, name)(*args, **kwargs)


class ScopetonException(Exception):
    def __init__(self, *args, **kwargs):
        super(Exception, self).__init__(*args, **kwargs)