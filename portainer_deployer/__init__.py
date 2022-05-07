from .config import config
from .utils import utils
from json import load
from os import path

info = load(open(path.join(path.abspath(path.dirname(__file__)), 'info.json')))
VERSION = info['version']
PHASE = info['phase']
PROG = info['info']['prog']

__all__ = ['config', 'utils']