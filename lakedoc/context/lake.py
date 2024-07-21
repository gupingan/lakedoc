import typing as t
from os import PathLike
from pathlib import Path
from lakedoc.utils import errors, file
from lakedoc.converters import LakeBaseConverter
from .base import LakeBaseContext


class LakeContext(LakeBaseContext):
    def __init__(self):
        self.options = {}
        self.converter_classes: t.Dict[str, LakeBaseConverter] = dict()
        self.converter_class: t.Optional[type(LakeBaseConverter)] = None

    def set_options(self, **options):
        self.options.update(options)

    def pick(self, target_type: t.Union[str]):
        """
        为当前上下文挑选指定的转换器类，该类将设置为属性 `converter_class` 的值
        :param target_type: 转换器对应的类型标签
        """
        if not isinstance(target_type, str):
            raise errors.LakeContentTypeError('参数 target_type', 'str', str(type(target_type)))

        if target_type not in self.converter_classes:
            raise errors.LakePickNotFoundError(target_type)

        self.converter_class = self.converter_classes[target_type]

    def content_convert(self, html: t.Union[str],
                        target_type: t.Union[str] = 'markdown',
                        uselast: t.Union[bool] = False):
        """将 HTML 内容通过指定的转换器转换为对应的内容"""
        if not html.strip():
            raise errors.LakeHTMLEmptyError

        if not self.converter_class or not uselast:
            self.pick(target_type)

        return self.converter_class(html, **self.options).convert()

    def content_convert_save(self, html: t.Union[str],
                             save_path: t.Union[str, Path, PathLike] = None,
                             target_type: t.Union[str] = 'markdown',
                             uselast: t.Union[bool] = False,
                             encoding: t.Union[str] = 'utf-8',
                             suffix: t.Union[str] = 'md', ):
        """将 HTML 内容通过指定的转换器转换为对应的内容并保存"""
        data = self.content_convert(html, target_type, uselast)
        save_path = save_path or Path('./')
        file.savefile(data, save_path, encoding, suffix)
        return data

    def read_convert(self, read_path: t.Union[str, Path, PathLike],
                     target_type: t.Union[str] = 'markdown',
                     uselast: t.Union[bool] = False,
                     encoding: t.Union[str] = 'utf-8'):
        """从 HTML 文件路径中读取内容并转换"""
        html = file.readfile(read_path, encoding=encoding)
        return self.content_convert(html, target_type, uselast)

    def read_convert_save(self, read_path: t.Union[str, Path, PathLike],
                          save_path: t.Union[str, Path, PathLike] = None,
                          target_type: t.Union[str] = 'markdown',
                          uselast: t.Union[bool] = False,
                          encoding: t.Union[str] = 'utf-8',
                          suffix: t.Union[str] = 'md', ):
        """从 HTML 文件路径中读取内容，通过转换后，保存到指定的路径"""
        data = self.read_convert(read_path, target_type, uselast, encoding)
        save_path = save_path or Path('./')
        file.savefile(data, save_path, encoding, suffix)
        return data

    def register(self, target_type: t.Union[str],
                 converter_class: t.Union[type(LakeBaseConverter)],
                 is_cover: t.Union[bool] = True):
        """
        注册外部的转换器
        :param target_type: 转换器类对应的类型标签，用于查找转换器类（pick/convert）
        :param converter_class: 外部的转换器类（继承于 LakeBaseConverter）
        :param is_cover: 开启后，类型标签一致的旧转换器类将直接被覆盖，默认开启
        """
        if not isinstance(target_type, str):
            raise errors.LakeContentTypeError('参数 target_type', 'str', str(type(target_type)))

        if is_cover:
            self.converter_classes[target_type] = converter_class
        else:
            self.converter_classes.setdefault(target_type, converter_class)
