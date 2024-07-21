from pathlib import Path
from lakedoc.utils import string

examples_folder = Path(__file__).parent.absolute().resolve()


def test_markdown():
    example_html_path = examples_folder / 'example.html'
    if not example_html_path.exists():
        print(string.color_string('Error！测试的 HTML 文件不存在，可能被删除或者打包丢失', 'red'))
        return None
    with example_html_path.open('r', encoding='utf-8') as fr:
        html = fr.read()

    print(f'''{string.color_string("Tips！转换成功的判断点：", "yellow")}
    1. 标题样式应正常显示，出现红色字体，最后章节存在超链接
    2. 总计 7 个章节、5 张图、2 个数学公式
    3. 仅存在一块关于快速排序的 js 代码''')

    example_images = [pf for pf in examples_folder.rglob('*') if pf.is_file() and pf.suffix in ('.png', '.svg')]

    example_values = {}
    for example_image in example_images:
        json_data = {
            'src': str(example_image.absolute().resolve()),
            'url': str(example_image.absolute().resolve()),
        }
        example_values[example_image.stem] = string.encode_card_value(json_data)

    if example_values:
        html = html.format(**example_values)

    from lakedoc.context import outer, LakeContext
    from lakedoc.converters.md_converter import MarkdownConverter
    if outer.context is None:
        context = LakeContext()
        context.register('markdown', MarkdownConverter, is_cover=False)
        outer.set_context(context)

    save_path = Path('./test_markdown.md')
    outer.context.content_convert_save(html, save_path)
    print(string.color_string(f'Success！转换后的文件路径：{str(save_path.absolute().resolve())}', 'green'))
