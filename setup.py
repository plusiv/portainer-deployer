from setuptools import setup, find_packages

PKG_NAME = 'portainer_deployer'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=PKG_NAME,
    version="0.0.1",
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
    python_requires=">=3.8.10",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            f"portainer-deployer={PKG_NAME}.app:main",
        ]
    }
)