<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/a0WbfH2.png" alt="Project logo"></a>
</p>

<h3 align="center">Portainer Deployer</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/Jorgmassih/portainer-deployer)](https://github.com/Jorgmassih/portainer-deployer/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/Jorgmassih/portainer-deployer/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)
</div>

---

<p align="center"> Portainer API simplified through command-line interface.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Configuring](#configuring)
- [Usage](#usage)
- [Built Using](#built_using)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)
- [Contributing](#contributing)

## ⚠️Important Notice⚠️
This is not an official [Portainer](https://www.portainer.io/about) software, it is just an Open Source tool to make an abstraction of Portainer's API.

## 🧐 About <a name = "about"></a>

__Portainer Deployer__ is a [Command-line interface](https://en.wikipedia.org/wiki/Command-line_interface) tool developed in Python to abstract some [Portainer](https://www.portainer.io/)'s features by using its [API](https://docs.portainer.io/v/ce-2.11/). The principal use case for this application is to manage Stacks in the CI/CD process, making it faster and easy.

## 🏁 Getting Started <a name = "getting_started"></a>

The first steps with Portainer Deployer are about installing and running your first commands. There are multiple installation methods, and they all will be listed in this section, but before you need to create the config directory and the config file.

```shell
$ mkdir -p /etc/pd-config # Or wherever you want
$ curl -o /etc/pd-config/default.conf https://raw.githubusercontent.com/Jorgmassih/portainer-deployer/main/portainer_deployer/app.conf.example
$ chgrp -R $USER /etc/pd-config && chmod -R 774 /etc/pd-config
```

This step should be executed before __all__ installation methods. If you have already done that, you can skip to the next steps.

> __Note__: Probably you will need to use `sudo` for creating the configuration folder and downloading the config template file
### Installation
[Python 3.8.x](https://docs.python.org/3/whatsnew/changelog.html) or greater is required for this project to run correctly.

You should be able to download it vía pip
```shell
$ python -m pip install --upgrade pip
$ python -m pip install portainer-deployer
$ portainer-deployer --version
```

If you want to avoid installing the `portainer-deployer` dependencies in your main python environment you can create a virtual environment before installing it:

```shell 
$ mkdir ~/portainer-deployer-env && cd ~/portainer-deployer-env
$ python -m venv pd_env && source ./pd_env/bin/activate
$ python -m pip install --upgrade pip
$ python -m pip install portainer-deployer
$ portainer-deployer --version
```

> For more information about virtual environments, please consult the [Official Documentation](https://docs.python.org/3.8/library/venv.html).


Since __Portainer Deployer__ is a command-line tool, you can invoke the application by running `portainer-deployer` after installation. We know that could be tedious to use the entire command to call the application, so, feel free to use an alias. e.g.

```shell
$ alias pd="portainer-deployer"
```

### Docker installation
This is the recommended method in case you don't have the required Python version or simply any installation of Python.

If you want to use the tool but without installing it in your environment to avoid overlapping with other applications, or if you are a __Windows__ user, this could be a fancy solution for you.

The idea is to create isolation for executing the applicatión in a recommended stable environment.

To get started with this method make sure you have a [stable version](https://docs.docker.com/release-notes/) of Docker installed by running `docker -v` and run the following snippet:

```shell
$ docker pull jorgmassih/portainer-deployer
$ docker run --rm -v path/to/config/file:/etc/pdcli/app.conf portainer-deployer --version # change --version for your desired command of portainer-deployer
```

Optionally you could use an `alias` for simplifying the command.
```shell
$ alias pd="docker run --rm -v path/to/config/file:/etc/pdcli/app.conf portainer-deployer"
$ pd --help
```

> __Binary installation__ will be available soon in the next releases. Please be patient.

### Post Installation
Before starting using Portainer Deployer normally, you will need to set some configurations to set up the connection with Portainer API. This can be easily managed by running `portainer-deployer config <config arguments goes here>`. You can go more in deep the [_config section_](#configuring) later. 
### Examples

Get all the Stacks from portainer
```shell
$ portainer-deployer get --all 
```
Get Stacks by its id
```shell
$ portainer-deployer get --id <random-id>
```
Deploy Stack from file by specifying its path
```shell
$ portainer-deployer deploy --path /path/to/my/docker-compose.yml --endpoint 45 --update-keys a.b.c=value e.f.g='[value2,value3...value4]' --name myStack
```
Deploy Stack passing string through  [standard input (stdin)](https://www.ibm.com/docs/en/ibm-mq/8.0?topic=commands-standard-input-output)
```shell
$ cat /path/to/my/docker-compose.yml | portainer-deployer deploy --endpoint 2 --name myStack
```
or
```shell
$ portainer-deployer deploy --endpoint 2 --name myStack "version: 3\n services:\n web:\n image:nginx"
```
> __Notice__ that using the _stdin_ can be faster than specifying a path to be processed by the program, otherwise, specifying a path grants access to some features such as modifying some keys in runtime by using the arguments `--update-keys` or `-u`. 

You can consult more information about allowed arguments and subcommands by running `portainer-deployer --help` or `portainer-deployer -h`.

## 🔧 Configuring <a name = "configuring"></a>
The first thing you need to set up is the configuration path by running `portainer-deployer config --config-path <YOUR ABSOLUTE PATH TO CONFIG FILE>`.

For example:
```shell
$ portainer-deployer config --config-path /etc/pd-config/default.conf 
Config path updated to: /etc/pd-config/default.conf
```

>__Note__: setting the config path is just valid for __all__ installation methods except __Docker installation method__.

### Setting configurations in the config file
There are two ways to go ahead with the configuration, the first one is by using the `config` sub-command to set all necessary variables. Another one is by editing directly the _config file_. The first one mentioned is strongly recommended to avoid misconfigurations.

### Using the `config` sub-command 
By Entering `portainer-deployer config --help` in your shell you will receive:
```shell
$ portainer-deployer config --help                                                                                                                           
usage: portainer-deployer config [-h] [--set SET [SET ...] | --get GET | --config-path CONFIG_PATH]

optional arguments:
  -h, --help            Show help message and exit.
  --set SET [SET ...], -s SET [SET ...]
                        Set a config value specifying the section, key and value. e.g. --set section.url='http://localhost:9000'
  --get GET, -g GET     Get a config value. e.g. --get section.port
  --config-path CONFIG_PATH, -c CONFIG_PATH
                        Set Portainer Deployer absulute config path. e.g. --config-path /abusolute/path/to/default.conf
```
> __Notice__ that you have to use the nomenclature of `section.key='new value'`.

The following table list the available sections:
| Section   | Description                                               |
|-----------|-----------------------------------------------------------|
| PORTAINER | All concerning configuration to Portainer API connection. |


Also, here is a list of all keys of the variables that can be set and gotten:
| Key        | Choices/Defaults | Description                                     |
|------------|------------------|-------------------------------------------------|
| url        |                  | Portainer URL to connect. e.g. https://10.0.0.3 |
| username   |                  | Username to connect to the API.                 |
| token      |                  | Token given by Portainer to connect to the API. |
| verify_ssl |   __yes__, no    | In case of "no" skip ssl verification.          |
### Examples
Set Portainer `url`
```shell
$ portainer-deployer config --set portainer.url='https://localhost:9443'
```

Get Portainer `username`
```shell
$ portainer-deployer config --get portainer.username
```
> __In the case of__ you try to set a variable not listed before, the operation won't take effect.

### Editing the `config file`
This method consists in editing the file you set by running `portainer-deployer config --config-path <YOUR PATH>` [at the moment of installation](#configuring), therefore you need the right privileges to access that file.

The config file is written in [INI](https://en.wikipedia.org/wiki/INI_file) format and looks like this:
```ini
# app.conf
[PORTAINER]
url = https://your-portainer.host.lab
username = <YOUR PORTAINER USERNAME>
token = <YOUR PORTAINER TOKEN>
verify_ssl = yes #It can be yes or not, [T,t]rue or [F,f]alse
```

> __Note__: If you are using the Docker installation method make sure to create a volume with the configuration file inside.

## 🎈 Usage <a name="usage"></a>
Portainer Deployer is composed of 4 main sub-commands:
- `get`
- `deploy`
- `remove`
- `config` _(explained in the past section)_

In this reading, we are going to focus on `get`, `deploy` and `remove` sub-commands.

### The `get` sub-command
By running `portainer-deployer get` you will be able to retrieve stacks information from Portainer by _name_ or _id_, you can retreive information of all stacks by setting the `--all` argument.

The command `portainer-deployer get -h` will result in:

```shell
$ portainer-deployer get --help                                                                        
usage: portainer-deployer get [-h] [--id ID | --name NAME | --all]

Get stack info from Portainer.

optional arguments:
  -h, --help            Show help message and exit.
  --id ID               Id of the stack to look for
  --name NAME, -n NAME  Name of the stack to look for
  --all, -a             Gets all stacks
```

### The `deploy` sub-command
This one allows to post stacks and run them in Portainer, it can be done by passing the string as `stdin` or passing the `path` to the `yml` file.

```shell
$ portainer-deployer deploy --help
usage: portainer-deployer deploy [-h] [--path PATH] [--name NAME] [--update-keys UPDATE_KEYS [UPDATE_KEYS ...]] --endpoint ENDPOINT [stack]

positional arguments:
  stack                 Docker Compose string for the stack

optional arguments:
  -h, --help            Show help message and exit.
  --path PATH, -p PATH  The path to Docker Compose file for the stack. An alternative is to pass the stack as a string.
  --name NAME, -n NAME  Name of the stack to look for.
  --update-keys UPDATE_KEYS [UPDATE_KEYS ...], -u UPDATE_KEYS [UPDATE_KEYS ...]
                        Modify the stack file by passing a list of key=value pairs, where the key is in dot notation. i.e. a.b.c=value1 d='[value2, value3]'
  --redeploy, -R        Re-deply in case of stacks exists.
  -y                    Accept redeploy and do not ask for confirmation before redeploying the stack.
  --endpoint ENDPOINT, -e ENDPOINT
                        Endpoint Id to deploy the stack.
```
You can redeploy a stack by using the `--redeploy` flag. This is useful to update an image rebuild. This feature requires a confirmation and can be accepted automatically and skipped with the `-y` flag.

### The `remove` sub-command
This sub-command allows you to remove a stack from Portainer by setting its `id` or `name` and the `endpoint` as well.

```shell
$ portainer-deployer remove --help
usage: portainer-deployer remove [-h] [--id ID | --name NAME] [--endpoint ENDPOINT] [-y]

Remove a stack from Portainer.

optional arguments:
  -h, --help            Show help message and exit.
  --id ID               Id of the stack remove
  --name NAME, -n NAME  Name of the stack to remove
  --endpoint ENDPOINT, -e ENDPOINT
                        Endpoint Id from the stack to remove.
  -y                    Accept removal action and do not ask for confirmation.
```
This sub-command also has a confirmation step, and can be accepted automatically and skipped with the `-y` flag.

## ⛏️ Built Using <a name = "built_using"></a>

- [Python 🐍](https://www.python.org/) - Core Programming Language
- [argparse](https://docs.python.org/3/library/argparse.html) - Main Python library for parsing arguments

## ✍️ Authors <a name = "authors"></a>

- [@jorgmassih👨‍💻](https://github.com/jorgmassih) - Idea & Initial work

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- [Portainer](https://www.portainer.io/about) and its development team
- My College Professor _Rodrigo Orizondo (@yoyirod)_ 🕊️🙏 for the inspiration
- The DevOps community

## 🤝 Contributing <a name = "contributing"></a>
I'm open to contributions!
If you are interested in collaborating, you can reach out to me via the info on [my bio](https://github.com/Jorgmassih).
