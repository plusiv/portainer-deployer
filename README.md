<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>

<h3 align="center">Portainer Deployer</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/Jorgmassih/portainer-deployer/issues)
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
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](../TODO.md)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## Disclaimer :warning:
This is not an official [Portainer]() software, it is just and Open Source tool to make an abstraction of the API.

## 🧐 About <a name = "about"></a>

This is a command line tool built in Python to use the [Portainer API]() to deploy Stacks and get Stacks Info throug Portainer API. The main use case for this application is to manage Stacks using the terminal in the CI/CD process, making it faster and easy.

## 🏁 Getting Started <a name = "getting_started"></a>

Since __Portainer Deployer__ is a command line tool, you can inoke the application by running `portainer-deployer` after installation.

You will need to set some params such as the configuration of connection to [Portainer API]() before start using the application. This can be easly managed by running `portainer-deployer config <config arguments goes here>`. We'll go more in deep later in this doc.

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
$ portainer-deployer deploy --path <path to docker-compose file> --endpoint <endpoint to deploy> --update-keys <a.b.c=value e.f.g=value2>
```


### Installing

A step by step series of examples that tell you how to get a development env running.

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo.

## 🔧 Configuring <a name = "configuring"></a>

First thing you need to set after installation is your Portainer Connection. There's two ways to manage configurations, the first one is by using the sub-command `config` to set all necessary variables. The another one is by editing directly the _config file_ located at `/path/to/config/file`. The first one mentioned is strongly recommended to avoid misconfigurations.

By sending `portainer-deployer config --help` in your shell you will receive:
```shell
$ portainer-deployer config -h                                                                                                                           
usage: portainerDeployer config [-h] [--set SET [SET ...] | --get GET]

optional arguments:
  -h, --help            show this help message and exit
  --set SET [SET ...], -s SET [SET ...]
                        Set a config value
  --get GET, -g GET     Get a config value
```

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## 🎈 Usage <a name="usage"></a>

Add notes about how to use the system.

## 🚀 Deployment <a name = "deployment"></a>

Add additional notes about how to deploy this on a live system.

## ⛏️ Built Using <a name = "built_using"></a>

- [MongoDB](https://www.mongodb.com/) - Database
- [Express](https://expressjs.com/) - Server Framework
- [VueJs](https://vuejs.org/) - Web Framework
- [NodeJs](https://nodejs.org/en/) - Server Environment

## ✍️ Authors <a name = "authors"></a>

- [@jorgmassih](https://github.com/jorgmassih) - Idea & Initial work

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Hat tip to anyone whose code was used
- Inspiration
- References
