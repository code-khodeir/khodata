"""Setup configuration for khodata package."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="khodata",
    version="0.1.0",
    author="khodata",
    description="Data intelligence pilot application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
    ],
    entry_points={
        "console_scripts": [
            "khodata=khodata.cli:main",
        ],
    },
)
