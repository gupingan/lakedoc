import typing as t
import re
import json
from urllib.parse import unquote, quote


def extract_integer(text: t.Union[str], default_: t.Union[int] = 0):
    """
    提取字符串中的整数（针对 11em、2em、2px 等字符串数据）

    :param text: 待提取的文本内容
    :param default_: 提取不到结果后返回的整数
    :return: 返回提取的整数（意味着浮点数将丢失部分精度）
    """
    digits = re.findall(r'\d+', text)
    value = ''.join(digits)
    return int(value) if value != '' else default_


def color_string(text: str, color: str = 'black') -> str:
    """
    将输入字符串转换为带有指定颜色的终端字符串

    :param text: 输入的字符串
    :param color: 指定的颜色，默认是黑色
    :return: 带有颜色的终端字符串
    """
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m'
    }
    color_code = colors.get(color, colors['black'])
    return f'{color_code}{text}{colors["reset"]}'


def decode_card_value(value: str) -> dict:
    """
    将 card 标签中的值解析
    :param value: 原始 value 值
    :return: 字典类型的数据
    """
    raw_card_value = value[5:]
    card_value = unquote(raw_card_value)
    card_data = json.loads(card_value)
    return card_data


def encode_card_value(json_data: dict) -> dict:
    """
    复原 card value 的值（重新编码）
    :param json_data: 字典数据
    :return: card 中编码的值
    """
    card_data = json.dumps(json_data)
    card_value = quote(card_data)
    raw_card_value = f'data:{card_value}'
    return raw_card_value


if __name__ == '__main__':
    print(extract_integer('em'))
    # cv value deleted
    # print(decode_card_value(cv))
