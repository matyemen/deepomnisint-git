#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="deepomnisint",
    version="3.0.0",
    author="Omnisint Team",
    description="أداة OSINT متقدمة للبحث عن اسم المستخدم مع استخراج بيانات عميق",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/omnisint/deepomnisint",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Intended Audience :: Information Technology",
    ],
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.9",
        "aiofiles>=23.0",
        "aiosqlite>=0.19",
        "beautifulsoup4>=4.12",
        "lxml>=4.9",
        "jinja2>=3.1",
        "fake-useragent>=1.4",
        "python-telegram-bot>=20.0",
        "colorama>=0.4",
        "rich>=13.0",
        "tqdm>=4.66",
        "Pillow>=10.0",
        "requests>=2.31",
        "pydantic>=2.0",
        "matplotlib>=3.7",
        "networkx>=3.1",
        "cryptography>=41.0",
    ],
    extras_require={
        "full": [
            "playwright>=1.40",
            "weasyprint>=60.0",
            "selenium>=4.15",
            "pyppeteer>=1.0",
        ],
        "dev": [
            "pytest>=7.0",
            "black>=23.0",
            "mypy>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "omnisint=deepomnisint:main",
        ],
    },
)
