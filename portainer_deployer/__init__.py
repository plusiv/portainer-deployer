from .config import config
from .utils import utils
from json import load
from os import path

versioning_info = load(open(path.join(path.abspath(path.dirname(__file__)), 'ver.json')))
VERSION = versioning_info['version']
PHASE = versioning_info['phase']
PROG = "portainer-deployer"

__all__ = ['config', 'utils']