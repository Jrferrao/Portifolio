#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="trading-bot",
    version="0.1.0",
    author="João Rafael Ferrão",
    author_email="jrferrao@gmail.com",
    description="Um sistema automatizado de trading com interface CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jrferrao/trading-bot",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Investment",
        "Intended Audience :: Financial and Insurance Industry",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
        "requests>=2.25.0",
        "ccxt>=2.0.0",  # Para integração com exchanges de criptomoedas
        "ta>=0.7.0",    # Biblioteca de análise técnica
        "python-dotenv>=0.19.0",
        "tabulate>=0.8.9",
        "argparse>=1.4.0",
    ],
    entry_points={
        "console_scripts": [
            "trading-bot=cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.md"],
    },
    zip_safe=False,
)