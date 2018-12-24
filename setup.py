import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simpletemplate",
    version="0.0.1-beta1",
    author="WangWei",
    author_email="2317073226@qq.com",
    description="简单灵活的代码生成模板引擎",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weixinfree/template",
    packages=setuptools.find_packages(),
    install_requires=[],
    entry_points={},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
