class LakeBaseContext(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __repr__(self):
        return f'<{self.__class__.__name__}: 0x{id(self):016X}>'


if __name__ == '__main__':
    context1 = LakeBaseContext()
    context2 = LakeBaseContext()
    print(context1 is context2)
