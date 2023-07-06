from scopeton import compat, glob, constants


def Inject():
    def inject_decorator(fn):
        if fn.__name__ == '__init__':
            # constructor injector
            def inject_wrapper(*args, **kwags):
                return glob.lastScope._inject_method_args(fn, args[0])
        else:
            inject_wrapper = fn

        setattr(inject_wrapper, constants.TO_INJECT_FLAG, 1)
        return inject_wrapper

    return inject_decorator
