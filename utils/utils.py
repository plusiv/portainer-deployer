from datetime import datetime as dt
from hashlib import sha256
import re
from yaml import Loader, load, dump
from re import match

def format_stack_list(stacks: list):
    """Format the list of stacks from Portainer and return a generator with it.

    Args:
        stacks (list): Raw list of stacks from Portainer.

    Yields:
        tuple: Formatted stack.
    """    
    for stack in stacks:
        stack_info = (
            stack['Id'], 
            stack['EndpointId'], 
            stack['Name'], 
            f"{dt.fromtimestamp(stack['CreationDate']).strftime('%m-%d-%y %H:%m')} by {stack['CreatedBy']}",
            f"{dt.fromtimestamp(stack['UpdateDate']).strftime('%m-%d-%y %H:%m')} by {stack['UpdatedBy']}"
        )
        yield stack_info

def generate_random_hash() -> str:
    """Generate a random hash.

    Returns:
        str: Random hash.
    """    
    random_hash = sha256(str(dt.now()).encode('utf-8')).hexdigest()
    return random_hash



def recursive_dict(dictionary: dict, keys: list, new_value=None) -> dict:
    if len(keys) == 1:
        dictionary[keys[0]] = new_value
    
    else:
        dictionary[keys[0]] = recursive_dict(dictionary[keys[0]], keys[1:], new_value)

    return dictionary



def edit_yml_file(path: str, key_group:str, new_value: str) -> str:
    """Edit a yaml file base in a chain of keys in dot notation. i.e. 'a.b.c'

    Args:
        path (str): Path to the yaml file.
        keys (str): Keys in dot notation. 
        new_value (str): New value to be set for the last key in the keys.
    """    
    data = {}
    keys = key_group.split('.')
    
    try:
        with open(path, 'r') as f:
            data = load(f, Loader=Loader)
        
        with open(path, 'w') as f:    
            try:
                recursive_dict(data, keys, new_value)
            
            except KeyError:
                return f"Wrong key secuence {keys}, not found in {path}."

            dump(data, f) 
    
    except FileNotFoundError:
        return f"File {path} not found."


def validate_key_value(pair: str) -> bool:
    """Validate a list of key=value pairs, where key in dot notation. i.e. a.b.c=value1 d=value2

    Args:
        pair (str): A key=value pair.

    Returns:
        bool: True if the pair is valid, False otherwise.
    """    
    if match(r'^[a-zA-Z0-9_\.]+=[a-zA-Z0-9_\.\-]+$', pair):
        return True

    return False