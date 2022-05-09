from setuptools import setup, find_packages
from json import load
from os import path

PKG_NAME = 'portainer_deployer'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

info = load(open(path.join(path.abspath(path.dirname(__file__)), f'{PKG_NAME}/info.json')))
version = info['version']
prog = info['info']['prog']


setup(
    name=PKG_NAME,
    version=version,
    author="Jorge A. Massih",
    author_email="jorgmassih@gmail.com",
    description="A command-line tool to abstract some Portainer's features by using its API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jorgmassih/portainer-deployer",
    project_urls={
        "Bug Tracker": "https://github.com/Jorgmassih/portainer-deployer/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Installation/Setup"
    ],
    install_requires=[
        "PyYAML~=6.0",
        "requests~=2.27.1",
    ],
    tests_require=['unittest'],
    python_requires=">=3.8.0",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            f"{prog}={PKG_NAME}.app:main",
        ]
    }
)