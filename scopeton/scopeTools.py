from scopeton import compat, constants


def flatten(lst):
    res = []
    for el in lst:
        if type(el) is list:
            res += flatten(el)
        else:
            res.append(el)
    return res


def get_class_name(cls):
    return cls.__name__ if hasattr(cls, "__name__") else str(cls)


def get_class_tree_qualifiers(cls):
    res = [get_bean_qualifier(k) for k in get_class_tree(cls)]
    res.reverse()
    return res


def rm_dups(lst):
    res = []
    for k in lst:
        if k not in res:
            res.append(k)
    return res


def get_class_tree(cls):
    return rm_dups(_get_class_tree(cls))


def _get_class_tree(cls):
    res = [cls]
    if type(cls) is not object and hasattr(cls, "__bases__") and cls.__bases__:
        res += flatten([_get_class_tree(parent) for parent in cls.__bases__])
    return res


def get_bean_qualifier(bean) -> str:
    if isinstance(bean, str):
        return bean
    from scopeton.objects import Bean
    if isinstance(bean, Bean):
        return bean.qualifier_tree[-1]
    if not hasattr(bean, "__name__"):
        return str(bean)
    return bean.__name__


def call_method_by_name(obj, name, *args, **kwargs):
    if hasattr(obj, name):
        return getattr(obj, name)(*args, **kwargs)


def get_injectables(instance):
    return [fn for fn in compat.get_methods(instance) if hasattr(fn, constants.TO_INJECT_FLAG)]


def get_annotations(instance):
    return {fn: getattr(fn, constants.ANNOTATED) for fn in compat.get_methods(instance) if hasattr(fn, constants.ANNOTATED)}


def set_annotation(fn, name, value):
    if not hasattr(fn, constants.ANNOTATED):
        setattr(fn, constants.ANNOTATED, {})
    annotations = getattr(fn, constants.ANNOTATED)
    annotations[name] = value


def get_methods_with_annotation(instance, name):
    annotations = get_annotations(instance)
    return [k for k in annotations if name in annotations[k]]


class ScopetonException(Exception):
    def __init__(self, *args, **kwargs):
        super(Exception, self).__init__(*args, **kwargs)
