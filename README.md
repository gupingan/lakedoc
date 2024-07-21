<p align="center">
  <h3 align="center">Welcome to Lakedoc</h3>
  <p align="center">
    <a href="https://github.com/gupingan/lakedoc/main.py">查看Demo</a>
    ·
    <a href="https://github.com/gupingan/lakedoc/issues">报告Bug</a>
    ·
    <a href="https://github.com/gupingan/lakedoc/issues">提出新特性</a>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/language-python-brightgreen" alt="Language">
  <a href="https://github.com/gupingan/lakedoc/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/gupingan/lakedoc.svg?style=flat-square" alt="Contributors">
  </a>
  <a href="https://github.com/gupingan/lakedoc/network/members">
    <img src="https://img.shields.io/github/forks/gupingan/lakedoc.svg?style=flat-square" alt="Forks">
  </a>
  <a href="https://github.com/gupingan/lakedoc/stargazers">
    <img src="https://img.shields.io/github/stars/gupingan/lakedoc.svg?style=flat-square" alt="Stargazers">
  </a>
  <a href="https://github.com/gupingan/lakedoc/issues">
    <img src="https://img.shields.io/github/issues/gupingan/lakedoc.svg?style=flat-square" alt="Issues">
  </a>
  <a href="https://github.com/gupingan/lakedoc/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/gupingan/lakedoc.svg?style=flat-square" alt="MIT License">
  </a>
</p>


## 目录

- [模块介绍](#模块介绍)
- [模块特性](#模块特性)
- [快速入门](#快速入门)
- [鸣谢](#鸣谢)

---

## 模块介绍

本模块基于 `beautifulsoup4` 所开发，在本地把 `Lake` 文档转换为指定格式的内容

```html
<!doctype lake>  
```

**遗憾**的是，当前仅支持 `Markdown` 格式(精力有限)，其余常用格式可以后续逐渐开发（欢迎各位开源社区的朋友们参与贡献）。

> PS：因为该模块并不是网络爬虫工具，所以数据源请自行寻找

## 模块特性

- 支持`markdown` 格式：已经适配大多数的文档，已采集简单到复杂的 `Lake Document` 共计测试 `29` 篇，还原度极高；
- 允许上层开发者`自定义转换器`、`注册转换器`、`使用转换器`等等一些更高级的行为；
- 使用非常简单，为上层提供一个接口 `convert`，入口函数进行伪重载，让使用更加方便。

![图片未加载](https://github.com/gupingan/lakedoc/raw/main/lakedoc/assets/arch-dark.png)

## 快速入门

请根据你的 `Python` 环境选择合适的模块安装命令。大多数情况下，下方的命令通用：

```bash
pip install lakedoc
```

安装失败时，请自行利用搜索引擎查阅解决方案。当然也可以在 [issues](https://github.com/gupingan/lakedoc/issues) 中共同解决，通常检查`镜像源`、`依赖版本`等常见问题。

在安装后，你可以使用如下的方式进行接口调用：

```python
import lakedoc

# lakedoc.test_markdown()  # 可以测试是否有效

# 假设 ./test_data/content1.html 是源文件，./test_data/test1.md 是保存路径
read_path = './test_data/content1.html'
save_path = './test_data/test1.md'

# 仅读取路径
print(lakedoc.convert(read_path))
# 转换路径内容并保存
lakedoc.convert(read_path, save_path)

# 仅转换内容
with open(read_path, 'r', encoding='utf-8') as fr:
     html = fr.read()
print(lakedoc.convert(html, is_file=False))
# 转换内容并保存
lakedoc.convert(html, save_path, is_file=False)

# 设置的并不是文件名，而是最顶行(首行)添加 `# xxxxxxx`
lakedoc.convert(read_path, save_path, title='# 🚛 超详细Redis7.X 安装以及快速入门加常见面试题讲解')

# 保存的路径既可以是指向文件，也可以是一个已存在的目录！
# 存储目录时，使用时间戳命名，默认文件后缀是 md，使用参数 suffix='pdf' 可修改
```

## 鸣谢


在此，我要特别感谢以下开源项目和其贡献者们，没有他们的努力和贡献，我的项目 `lakedoc` 将寸步难行：

- **Beautiful Soup 4**：[Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) 是一个非常优秀的 Python 库，用于从 HTML 和 XML 文件中提取数据。感谢作者 Leonard Richardson 以及所有为该项目做出贡献的开发者们。

* **Markdownify**：[Markdownify](https://github.com/matthewwithanm/python-markdownify) 是一个将 HTML 转换为 Markdown 的 Python 库。感谢 Matthew Tretter 及所有贡献者们的努力，使得我们能够轻松地将 HTML 内容转换为 Markdown 格式。

