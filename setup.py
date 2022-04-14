from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="portainer-deployer",
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
        "Operating System :: Linux",
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
            "portainer-deployer=portainer_deployer.app:main",
        ]
    },
    package_data={"portainer_deployer": [".env"]}
)