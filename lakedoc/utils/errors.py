import typing as t
from pathlib import Path
from os import PathLike
from lakedoc.utils import string


class LakeBaseError(Exception):
    def __init__(self, info):
        super().__init__(self)
        self.error_info = f'{info}'

    def __str__(self):
        return string.color_string(self.error_info, color='red')

    def __repr__(self):
        return f'<{self.__class__.__name__}: 0x{id(self):016X}>'


class LakeFileNotFoundError(LakeBaseError, FileNotFoundError):
    def __init__(self, path: t.Union[str, Path, PathLike]):
        info = f'指定的文件路径`{str(path.absolute().resolve())}`不存在'
        super().__init__(info)


class LakeIsNotFileError(LakeBaseError):
    def __init__(self, path: t.Union[str, Path, PathLike]):
        info = f'路径`{str(path.absolute().resolve())}`并非是文件类型'
        super().__init__(info)


class LakeContentTypeError(LakeBaseError, TypeError):
    def __init__(self, name: t.Union[str], expected_type: t.Union[str], actual_type: t.Union[str]):
        info = f'{name} 仅支持`{expected_type}`类型，实际上却是`{actual_type}`类型'
        super().__init__(info)


class LakeContextError(LakeBaseError):
    pass


class LakePickNotFoundError(LakeContextError):
    def __init__(self, target_type: t.Union[str]):
        info = f'类型`{target_type}`的转换器并未注册'
        super().__init__(info)


class LakeHTMLEmptyError(LakeContextError):
    def __init__(self):
        info = '转换时传入的 HTML 内容不能为空'
        super().__init__(info)


class LakeBuilderNotFoundError(LakeContextError):
    def __init__(self, builder: t.Union[str]):
        info = f'树构建器: {builder} 不存在，可尝试运行命令：`pip install {builder}`'
        super().__init__(info)
