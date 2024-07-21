"""
Markdown 转换器

作者：
    Gu pingan(顾平安)[g332920287@foxmail.com]

特性：
    - 能够良好的处理换行和段落的缩进（还原率极高）
    - 支持转换的基本语法：标题、段落、粗/斜体、引用、分隔线、超链接、静态图片、Emoji、GIF图……
    - 支持转换的进阶语法：代码块、列表、内嵌 HTML、数学公式……
    - 大多数文本的转换将携带颜色（前景色、背景色）转换，表格将直接嵌入到 Markdown 内容中
    - 解决相邻<em>标签转换后的斜体二义性、相邻的<strong>标签转换后的粗体二义性两个问题

注意：
    部分语法暂未适配，可能存在失效（丢失、直接显示、乱码），如果需要适配，请提供文档库给我，并标明相关位置
"""

import typing as t
from bs4 import BeautifulSoup, FeatureNotFound
from markdownify import MarkdownConverter as MDConverter
from lakedoc.utils import string, errors
from .base import LakeBaseConverter


class MarkdownConverter(LakeBaseConverter):
    class ParticularConverter(MDConverter):
        def __init__(self, parent_converter: 'MarkdownConverter'):
            """
            针对部分标签特殊转换
            处理方法中必须含有三个参数 el, text, convert_as_inline
            """
            super().__init__()
            self.parent_converter = parent_converter

        def convert_font(self, el, text, convert_as_inline):
            return str(el) if text else ''

        def convert_card(self, el, text, convert_as_inline):
            card_type = el.attrs['name']
            if card_type == 'hr':
                return '---\n'
            elif card_type in ('image', 'flowchart2', 'board'):
                card_data = string.decode_card_value(el.attrs.get('value', ''))
                src = card_data.get('src', '')
                return f'![图片未加载]({src})\n'
            elif card_type == 'table':
                card_data = string.decode_card_value(el.attrs.get('value', ''))
                return f'{card_data["html"]}\n'
            elif card_type == 'codeblock':
                card_data = string.decode_card_value(el.attrs.get('value', ''))
                mode = card_data.get('mode', '')
                code = card_data.get('code', '')
                return f'\n```{mode}\n{code}\n```\n'
            elif card_type == 'diagram':
                card_data = string.decode_card_value(el.attrs.get('value', ''))
                src = card_data.get('url', '')
                return f'![图片未加载]({src})\n'
            elif card_type == 'math':
                card_data = string.decode_card_value(el.attrs.get('value', ''))
                code = card_data.get('code', '')
                if 'center' in el.parent.get("style", ''):
                    return f'$$\n{code}\n$$'
                return f'$${code}$$'
            elif card_type == 'yuqueinline':
                card_data = string.decode_card_value(el.attrs.get('value', ''))
                src = card_data.get('src', '')
                title = card_data.get('detail', {}).get('title', '未获取到超链接显示名')
                elicit_type = card_data.get('detail', {}).get('type', 'doc')
                if elicit_type.lower() == 'doc':
                    doc_icon = str((self.parent_converter.assets / 'doc-type-default.svg').absolute().resolve())
                    return f'![图标]({doc_icon})[{title}]({src})'
                return f'[{title}]({src})'
            elif card_type == 'bookmarkInline':
                card_data = string.decode_card_value(el.attrs.get('value', ''))
                src = card_data.get('src', '')
                title = card_data.get('detail', {}).get('title', '未获取到超链接显示名')
                icon_url = card_data.get('detail', {}).get('icon')
                if icon_url:
                    return f'![图标]({icon_url})[{title}]({src})'
                return f'[{title}]({src})'
            elif card_type == 'imageGallery':
                card_data = string.decode_card_value(el.attrs.get('value', ''))
                image_list = card_data.get('imageList', [])
                image_gallery = []
                total_width = sum(image.get('original', {}).get('width', 0) for image in image_list)
                for image in image_list:
                    image_title = image.get('title', '图片无标题')
                    image_src = image.get('src')
                    width = image.get('original', {}).get('width', 0)
                    if not width or total_width <= 0:
                        image_gallery.append(f'![图片-{image_title}]({image_src})')
                    else:
                        width_percent = int((width / total_width) * 100) - 1
                        image_gallery.append(f'<img src="{image_src}" alt="{image_title}"  width="{width_percent}%"/>')
                return f"{''.join(image_gallery)}\n"
            return ''

        def convert_li(self, el, text, convert_as_inline):
            indent = 0
            if el.parent and el.parent.name in ('ul', 'ol'):
                if 'data-lake-indent' in el.parent.attrs:
                    indent = int(el.parent.attrs['data-lake-indent'])
                    # print(el.parent, indent)

            prefix = "\t" * indent

            raw = super().convert_li(el, text, convert_as_inline)
            return f'{prefix}{raw}'

        def convert_hn(self, n, el, text, convert_as_inline):
            raw = super().convert_hn(n, el, text, convert_as_inline)
            return f'\n{raw}'

        def convert_sub(self, el, text, convert_as_inline):
            return str(el)

        def convert_sup(self, el, text, convert_as_inline):
            return str(el)

    def __init__(self, raw_html: t.Union[str], builder: t.Union[str] = None,
                 title: t.Union[str] = None,
                 extract_tags: t.Set[str] = None):
        """
        Lake Doc -> Markdown Doc
        :param raw_html: 未经过处理的 HTML 内容（最原生的）
        :param builder: bs4 的树构建器，默认为 'html.parser'（options 参数）
        :param title: 指定设置转换后 Markdown内容顶行的标题，默认为 None（options 参数）
        :param extract_tags:
            处理 html 时应该删除哪些标签，默认为 {'meta', 'link', 'script', 'style'}（options 参数）
        """
        super().__init__(raw_html)
        self.builder = builder or 'html.parser'
        self.title = title
        self.extract_tags = extract_tags or {'meta', 'link', 'script', 'style'}
        self.soup = self.create_bs4soup()

    def convert(self) -> t.Union[str]:
        html_data = self.create_html()
        md_data = self.ParticularConverter(self).convert(html_data)
        md_data = self.add_title(md_data)
        return md_data

    def create_html(self) -> t.Union[str]:
        """
        处理、创建 更加合法的 HTML 内容

        :return: HTML 字符串内容
        """
        for tag in self.soup.find_all(True):
            self.render_styles(tag)

            if tag.name in self.extract_tags:
                tag.extract()

        return str(self.soup)

    def create_bs4soup(self) -> t.Union[BeautifulSoup]:
        """
        创建 soup 对象（导入、加工、返回）

        :return: BeautifulSoup 对象
        """
        raw_data = self.raw_html.replace('\n', '').replace('\r', '').strip()
        try:
            soup = BeautifulSoup(raw_data, self.builder)

            # feature: 合并相邻的 em 标签，防止转换后出现 *ab**cd* 这种难以解析的 md 语法
            for em_tag in soup.find_all('em'):
                next_sibling = em_tag.find_next_sibling()
                # 如果存在相邻<em>标签
                while next_sibling and next_sibling.name == 'em':
                    # 将其子元素拓展到到第1个<em>标签中
                    em_tag.extend(next_sibling.contents)
                    next_sibling.extract()
                    next_sibling = em_tag.find_next_sibling()

            for strong_tag in soup.find_all('strong'):
                next_sibling = strong_tag.find_next_sibling()
                while next_sibling and next_sibling.name == 'strong':
                    strong_tag.extend(next_sibling.contents)
                    next_sibling.extract()
                    next_sibling = strong_tag.find_next_sibling()

            return soup
        except FeatureNotFound:
            raise errors.LakeBuilderNotFoundError(self.builder)

    def render_styles(self, el):
        """
        根据 element 对象，渲染出对应的合法样式
        :param el: bs4 中的 PageElement 对象
        """
        if 'style' not in el.attrs:
            return None

        raw_style = el.attrs['style']
        raw_styles = [si.strip() for si in raw_style.split(';') if ':' in si]
        styles: t.Dict[str, str] = {si.split(':', 1)[0].strip(): si.split(':', 1)[-1].strip() for si in raw_styles}
        if 'color' in styles or 'background-color' in styles:
            if el.parent and el in el.parent.contents and el.string:
                new_tag = BeautifulSoup(f'<font style="{raw_style}">{el.string}</font>',
                                        self.builder).font
                el.replace_with(new_tag)

        if 'text-indent' in styles:
            text_indent = string.extract_integer(styles['text-indent'])
            prefix = "<span>&#8195;</span>" * text_indent
            if el.parent:
                el.insert_before(BeautifulSoup(prefix, self.builder))
        elif 'padding-left' in styles:
            text_indent = string.extract_integer(styles['padding-left'])
            prefix = "<span>&#8195;</span>" * text_indent
            if el.parent:
                el.insert_before(BeautifulSoup(prefix, self.builder))

    def add_title(self, data: t.Union[str]):
        """
        如果传入的数据不是 None，那么将其添加到转换内容顶部（支持 md 语法）
        :param data: title 顶行数据（一般是文档的标题名称）
        :return: 处理好的 Markdown 内容
        """
        if self.title is not None:
            if data.startswith('\n\n'):
                data = f'{self.title}{data[1:]}'
            else:
                data = f'{self.title}\n{data}'
        else:
            if data.startswith('\n\n'):
                data = data[1:]

        return data
