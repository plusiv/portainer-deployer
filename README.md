<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>

<h3 align="center">Portainer Deployer</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/Jorgmassih/portainer-deployer)](https://github.com/Jorgmassih/portainer-deployer/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/Jorgmassih/portainer-deployer/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)
</div>

---

<p align="center"> Portainer API simplified through command line.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Installation](#installation)
- [Configuring](#configuring)
- [Usage](#usage)
- [Built Using](#built_using)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## :warning:Important Notice:warning:
This is not an official [Portainer](https://www.portainer.io/) software, it is just and Open Source tool to make an abstraction of its API.

## 🧐 About <a name = "about"></a>

__Portainer Deployer__ is a command-line tool developed in Python to abstract some [Portainer](https://www.portainer.io/)'s features by using its [API](https://docs.portainer.io/v/ce-2.11/). The principal use case for this application is to manage Stacks using the terminal in the CI/CD process, making it faster and easy.

## 🏁 Getting Started <a name = "getting_started"></a>

Since __Portainer Deployer__ is a command line tool, you can invoke the application by running `portainer-deployer` after installation. We know could be tedious using the entire command to call the application, so, feel free to use an alias. e.g.

```shell
$ alias pd="portainer-deployer"
```

Before starting using Portainer Deployer, you will need to set some configurations to set up the connection with Portainer API. This can be easily managed by running `portainer-deployer config <config arguments goes here>`. You can go more in deep the [_config section_](#configuring). 
### Examples

Get all the Stacks from portainer
```shell
$ portainer-deployer get --all 
```
Get Stacks by its id
```shell
$ portainer-deployer get --id <random-id>
```
Deploy Stack from file
```shell
$ portainer-deployer deploy --path /path/to/my/docker-compose.yml --endpoint 45 --update-keys a.b.c=value e.f.g='[value2,value3...value4]' --name myStack
```

Deploy Stack passing string to stdin
```shell
$ cat /path/to/my/docker-compose.yml | portainer-deployer deploy --endpoint 2 --name myStack
```

You can consult more information about allowed arguments and subcommands by entering `portainer-deployer --help` or `portainer-deployer -h`.

## Installing
There is some intallation methods for this application and they will be listed down below:

### Python installation
This method requires a modern version of [Python 3]() already installed.

```shell 
$ git clone https://github.com/Jorgmassih/portainer-deployer.git
$ python -m pip install -e .
$ portainer-deployer --version
```

If you want to avoid installing the `portainer-deployer` dependencies in your main python environment you can create a virtual environment before installing it:

```shell 
$ git clone https://github.com/Jorgmassih/portainer-deployer.git
$ cd portainer-deployer
$ python -m venv pd_env
$ source ./pd_env/bin/activate
$ python -m pip install -e .
$ portainer-deployer --version
```

### Docker installation
This is the recommended method in case you don't have the required Python version or simply any installation of Python.

If you want to use the tool but without installing it in your environment to avoid overlaping with others applications or if you are a __Windows__ user, this could be a fancy solution for you.

The idea is create an isolation for executing the applicatión in its recommended environment.

To get started with this method make you have a [stable version](https://docs.docker.com/release-notes/) of Docker installed by running `docker -v`.

```shell
$ docker pull jorgmassih/portainer-deployer
$ docker run --rm -v path/to/config/file:/etc/pdcli/app.conf portainer-deployer --version # change --version for your desired command of portainer-deployer
```

Optionally you could use an `alias` for simplifying the command.
```shell
$ alias pd="docker run --rm -v path/to/config/file:/etc/pdcli/app.conf portainer-deployer"
$ pd --help
```

> Note: Binary installation will be available soon in next releases.
## 🔧 Configuring <a name = "configuring"></a>

There's two ways to go ahead with the configuration, the first one is by using the `config` sub-command to set all necessary variables. The another one is by editing directly the _config file_. The first one mentioned is strongly recommended to avoid misconfigurations.

### Using `config` sub-command 
By Entering `portainer-deployer config --help` in your shell you will receive:
```shell
$ portainer-deployer config -h                                                                                                                           
usage: portainer-deployer config [-h] [--set SET [SET ...] | --get GET]

optional arguments:
  -h, --help            show this help message and exit
  --set SET [SET ...], -s SET [SET ...]
                        Set a config value specifying the section, key and value. e.g. --set section.url='http://localhost:9000'
  --get GET, -g GET     Get a config value. e.g. --get section.port
```
> __Notice__ that you have to use the nomenclature of `section.key='new value'`.

The following table list the available sections:
| Section   | Description                                               |
|-----------|-----------------------------------------------------------|
| PORTAINER | All concerning configuration to Portainer API connection. |


Also, here is a list of all keys of the variables that can be set and get:
| Variable Key | Choices/Defaults | Description                                     |
|----------|------------------|-------------------------------------------------|
| url      |                  | Portainer URL to connect. e.g. https://10.0.0.3 |
| port     |                  | Port to reach out Portainer host.               |
| username |                  | Username to connect to the API.                 |
| token    |                  | Token given by Portainer to connect to the API. |
| ssl      | __yes__, no     | Use SSL for secure connections.                 |

### Examples
Set Portainer `url`
```shell
$ portainer-deployer config --set portainer.url='https://localhost'
```

Get Portainer `port`
```shell
$ portainer-deployer config --get portainer.port
```
> __In case of__ you try to set a variable not listed beffore, the operation won't take effect.

### Editing directly the `config file`
Usually the app configuration is located at `/etc/portainer-deployer/app.conf` and is in [INI](https://en.wikipedia.org/wiki/INI_file) format, so you would have the right permissions to edit the config file, which looks like: 

```ini
# app.conf
[PORTAINER]
url = https://portainer.host.lab
port = 9443
username = portainer-deployer
token = fal324ASDdjhdfasdjfaADSFADfasdgasd-
ssl = yes
```

## 🎈 Usage <a name="usage"></a>
Portainer Deployer is composed by 3 main sub-commands:
- `get`
- `deploy`
- `config` _(explained in the past section)_

In this reading we are going to focus in `get` and `deploy` sub-commands.

### The `get` sub-command
By entering `portainer-deployer get` you will be able to retrive stacks information from Portainer. The command `portainer-deployer get -h` will result in:

```shell
usage: portainer-deployer get [-h] [--id ID | --name NAME | --all]

Get a stack info from portainer.

optional arguments:
  -h, --help            show this help message and exit
  --id ID               Id of the stack to look for
  --name NAME, -n NAME  Name of the stack to look for
  --all, -a             Gets all stacks
```

### The `deploy` sub-command
This one allows to post stacks and run them in Portainer, it can be done by passing the string as `stdin` or by passing the `path` to the `yml` file.

```shell
usage: portainer-deployer deploy [-h] [--path PATH] [--name NAME] [--update-keys UPDATE_KEYS [UPDATE_KEYS ...]] [--endpoint ENDPOINT] [stack]

positional arguments:
  stack                 Docker Compose string for the stack

optional arguments:
  -h, --help            show this help message and exit
  --path PATH, -p PATH  The path to Docker Compose file for the stack. An alternative to pass the stack as string
  --name NAME, -n NAME  Name of the stack to look for
  --update-keys UPDATE_KEYS [UPDATE_KEYS ...], -u UPDATE_KEYS [UPDATE_KEYS ...]
                        Modify the stack file/string by passing a list of key=value pairs, where the key is in dot notation. i.e. a.b.c=value1
                        d='[value2, value3]'
  --endpoint ENDPOINT, -e ENDPOINT
                        Endponint Id to deploy the stack

```


## ⛏️ Built Using <a name = "built_using"></a>

- [Python 🐍](https://www.python.org/) - Core Programming Language
- [argparse](https://docs.python.org/3/library/argparse.html) - Main Python library for parsing arguments

## ✍️ Authors <a name = "authors"></a>

- [@jorgmassih](https://github.com/jorgmassih) - Idea & Initial work

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- [Portainer]() and its development team
- My Collage Professor _Rodrigo Orizondo (@yoyirod)_ 🕊️🙏 for the inspiration
- The DevOps community
