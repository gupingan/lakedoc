from inspect import getfullargspec


class Function(object):
    def __init__(self, fn):
        self.fn = fn

    def __repr__(self):
        return f'<Function {self.fn.__name__} at 0x{id(self):016X}>'

    def __call__(self, *args, **kwargs):
        fn = Namespace.get(self.fn, *args)
        if not fn:
            raise RuntimeError("No matching function found.")
        return fn(*args, **kwargs)

    def key(self, args=None):
        if args is None:
            args = getfullargspec(self.fn).args

        return tuple([
            self.fn.__module__,
            self.fn.__class__,
            self.fn.__name__,
            len(args),
        ])


class Namespace(object):
    _mappings = dict()

    @classmethod
    def register(cls, fn):
        func = Function(fn)
        key = func.key()
        cls._mappings[key] = fn
        return func

    @classmethod
    def get(cls, fn, *args):
        func = Function(fn)
        key = func.key(args=args)
        return cls._mappings.get(key)


def overload(fn):
    """overload is the decorator that wraps the function and returns a callable object of type Function."""
    return Namespace.register(fn)


if __name__ == '__main__':
    @overload
    def add(a: int, *, b: int = 2) -> int:
        return a + b


    def sub(a: int, *, b: int = 2) -> int:
        return a - b


    @overload
    def add(a: int, b: int, *, c: int = 2) -> int:
        return a + b + c


    try:
        print(add)
        print(sub)
        result1 = add(1, b=4)
        print(f"add(1, 4) = {result1}")  # Expected output: 3

        result2 = add(1, 2, c=3)
        print(f"add(1, 2, 3) = {result2}")  # Expected output: 6
    except RuntimeError as e:
        print(e)
