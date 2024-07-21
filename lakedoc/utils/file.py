import typing as t
import time
from pathlib import Path
from os import PathLike
from lakedoc.utils import errors


def readfile(path: t.Union[str, Path, PathLike], encoding: t.Union[str] = 'utf-8'):
    """
    从指定路径读取字节内容并解码后输出

    :param path: 读取文件的路径（只能传入文件路径）
    :param encoding: 指定读取文件时的解码格式，默认：utf-8
    :return: 指定文件中的内容（字符串）
    """

    path = Path(path)

    if not path.exists():
        raise errors.LakeFileNotFoundError(path)

    if not path.is_file():
        raise errors.LakeIsNotFileError(path)

    with open(path, 'rb') as fr:
        content = fr.read().decode(encoding=encoding)

    return content


def savefile(content: t.Union[str, bytes], path: t.Union[str, Path, PathLike],
             encoding: t.Union[str] = 'utf-8', suffix: t.Union[str] = 'md'):
    """
    将指定内容以字节流形式保存到指定路径

    :param content: 待保存的内容（可以是字符串或者字节串）
    :param path: 指定保存的路径（可以是目录或者文件路径）
    :param encoding: 保存字符串内容的编码，默认：utf-8
    :param suffix: 文件类型后缀名 比如（md[默认]、txt）
    :return:
    """
    path = Path(path)

    if path.is_dir():
        path = path / f'{int(time.time())}.{suffix}'

    if isinstance(content, bytes):
        data = content
    elif isinstance(content, str):
        data = content.encode(encoding=encoding)
    else:
        raise errors.LakeContentTypeError(f'参数 content', 'str/bytes', str(type(content)))

    with open(path, 'wb') as fw:
        fw.write(data)
