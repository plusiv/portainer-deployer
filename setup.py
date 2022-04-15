from os import environ, path, getenv, makedirs
from shutil import copy
from setuptools import setup, find_packages
from setuptools.command.install import install

PKG_NAME = 'portainer_deployer'
CONF_DEFAULT_PATH = f'/etc/{PKG_NAME}'

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    
    @property
    def __app_installation_path(self):
        """Returns the installation path of the application."""
        return path.join(self.install_lib, PKG_NAME)

    @property
    def __env_file_path(self):
        """Returns the path to the .env file."""
        return path.join(self.__app_installation_path, '.env')
    
    @property
    def config_path_dir(self):
        """Returns the path to the config directory."""
        return f'{getenv(f"{PKG_NAME.upper()}_CONF_PATH")}' \
            if getenv(f'{PKG_NAME.upper()}_CONF_PATH') \
            else CONF_DEFAULT_PATH
    
    
    def create_env_file(self):
        """Create the .env file in the package directory."""
        
        with open(self.__env_file_path, 'w') as f:
            f.write('[CONFIG]\n')
            f.write(f'PATH_TO_CONFIG={self.config_path_dir}/app.conf\n')
            
    def create_config_file(self):
        """Creates the config directory."""
        
        # Get current absolute path of the directory
        current_path = path.abspath(path.dirname(__file__))

        config_template_path = path.join(current_path, PKG_NAME)
        config_template_path = path.join(config_template_path, 'app.conf.example')

        # Create the config directory if it doesn't exist'
        try:
            if not path.exists(self.config_path_dir):
                makedirs(self.config_path_dir)

            if not path.exists(path.join(self.config_path_dir, 'app.conf')):
                # Copy the config file to in config directory
                copy(config_template_path, path.join(self.config_path_dir, 'app.conf'))


        except OSError as e:
            print(f'Creation of the directory {self.config_path_dir} failed. Error: {e}')
            print('Home directory will be used instead.')
            
            try:
                home_dir = path.expanduser('~')
                config_dir = path.join(home_dir, f'.{PKG_NAME}')
                if not path.exists(home_dir):
                    makedirs(config_dir)

                environ[f"{PKG_NAME.upper()}_CONF_PATH"] = config_dir
            
                if not path.exists(path.join(config_dir, 'app.conf')):
                    # Copy the config file in the config directory
                    copy(config_template_path, path.join(config_dir, 'app.conf'))

            except OSError as e:
                print(f'Creation of the directory {home_dir}/.{PKG_NAME} failed. Error: {e}')
                print('Installation will be aborted. You could try to re-run the installation or app may crash.')
                exit(1)
        
    def run(self):
        install.run(self)
        self.create_config_file()
        self.create_env_file()

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
    packages=find_packages(where=PKG_NAME, include=['*']),
    entry_points={
        "console_scripts": [
            f"portainer-deployer={PKG_NAME}.app:main",
        ]
    },
    cmdclass={'install': PostInstallCommand}
)