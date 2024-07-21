"""**Welcome To LakeDoc**

(*^▽^*) `Open source is limited, but thinking is limitless.`

Convert Lake documents (Yuque) into the specified format (currently supports md files).
Able to adapt to most Lake documents.

**Author Info:**
  - **Name:** Gu Pingan(顾平安)
  - **Email:** g332920287@foxmail.com

**License:** MIT
"""

__version__ = '1.0.1'
__author__ = 'Gu Pingan'

from .converters import LakeBaseConverter
from .converters.md_converter import MarkdownConverter
from .context import LakeBaseContext, LakeContext, outer
from .examples import test_markdown
from .utils import file, string

convert = outer.convert
context = LakeContext()
context.register('markdown', MarkdownConverter, is_cover=False)
outer.set_context(context)
