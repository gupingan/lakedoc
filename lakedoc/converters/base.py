import typing as t
from pathlib import Path


class LakeBaseConverter(object):
    def __init__(self, raw_html: t.Union[str]):
        self.raw_html = raw_html
        self.assets = Path(__file__).parent.parent / 'assets'

    def __repr__(self):
        return f'<{self.__class__.__name__}: 0x{id(self):016X}>'

    def convert(self) -> t.Union[str, bytes]:
        raise NotImplementedError
