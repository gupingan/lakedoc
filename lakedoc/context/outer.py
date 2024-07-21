import typing as t
from pathlib import Path
from os import PathLike
from lakedoc.utils import function
from .lake import LakeContext

context: t.Optional[LakeContext] = None


def set_context(context_: t.Optional[LakeContext]):
    """设置当前的上下文内容"""
    global context
    context = context_


@function.overload
def convert(html_or_path: t.Union[str, Path, PathLike], *,
            target_type='markdown', uselast=False, encoding='utf-8', is_file=True, **options):
    """
    将 HTML 转换并返回

    :param html_or_path: 读取的路径，仅支持文件（未校验 HTML，非法文件后果自负）
    :param target_type: 转换器对应的类型标签，用于查找转换器类，默认：markdown
    :param uselast: 开启后则使用最新 pick 的转换器类（如果没有，将自动 pick），默认不开启
    :param encoding: 读取文件时指定的编码，默认：utf-8
    :param is_file: 读取的通道。未开启时读取传入的内容，默认开启（读取文件）
    :return: 转换后的文本内容或者字节内容
    """
    context.set_options(**options)
    if is_file:
        return context.read_convert(html_or_path, target_type, uselast, encoding)
    return context.content_convert(html_or_path, target_type, uselast)


@function.overload
def convert(html_or_path: t.Union[str, Path, PathLike],
            save_path: t.Union[str, Path, PathLike],
            *,
            target_type: t.Union[str] = 'markdown',
            uselast: t.Union[bool] = False,
            encoding: t.Union[str] = 'utf-8',
            suffix: t.Union[str] = 'md',
            is_file: t.Union[bool] = True,
            **options):
    """
    将 HTML 转换后并保存

    :param html_or_path: 可以是 HTML 文件路径或者 HTML 内容（设置 is_file 为 False）
    :param save_path: 保存的路径，支持目录或者文件
    :param target_type: 转换器对应的类型标签，用于查找转换器类，默认：markdown
    :param uselast: 开启后则使用最新 pick 的转换器类（如果没有，将自动 pick），默认不开启
    :param encoding: 读写文件时指定的编码，默认：utf-8
    :param suffix: 当保存路径是一个文件夹时，保存时采用的文件后缀，默认：md
    :param is_file: 读取的通道。未开启时读取传入的内容，默认开启（读取文件）
    :return: 转换后的文本内容或者字节内容
    """
    context.set_options(**options)
    if is_file:
        return context.read_convert_save(html_or_path, save_path, target_type, uselast, encoding, suffix)
    return context.content_convert_save(html_or_path, save_path, target_type, uselast, encoding, suffix)
