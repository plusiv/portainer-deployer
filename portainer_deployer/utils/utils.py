from datetime import datetime as dt
from hashlib import sha256
from yaml import Loader, load, dump
from re import match
from typing import Any

def format_stack_info_generator(stacks: list):
    """Format the list of stacks from Portainer and return a generator with it.

    Args:
        stacks (list): Raw list of stacks from Portainer.
    
    Yields:
        tuple: Tuple of some stack info values.
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


def format_stack_info(stack: dict):
    """Format the stack info from Portainer.

    Args:
        stack (dict): Raw stack info from Portainer.
    
    Returns:
        tuple: Tuple of some stack info values.
    """
    if len(stack) == 0:
        return ()

    return (
        stack['Id'], 
        stack['EndpointId'], 
        stack['Name'], 
        f"{dt.fromtimestamp(stack['CreationDate']).strftime('%m-%d-%y %H:%m')} by {stack['CreatedBy']}",
        f"{dt.fromtimestamp(stack['UpdateDate']).strftime('%m-%d-%y %H:%m')} by {stack['UpdatedBy']}"
    )

def generate_random_hash() -> str:
    """Generate a pseudo-random hash.

    Returns:
        str: Random hash.
    """    
    random_hash = sha256(str(dt.now()).encode('utf-8')).hexdigest()
    return random_hash



def recursive_dict(dictionary: dict, keys: list, new_value: Any=None) -> dict:
    """Recursively set a value in a dictionary.

    Args:
        dictionary (dict): Target dictionary.
        keys (list): Keys to access the value.
        new_value (Any, optional): Value to be set. Defaults to None.

    Returns:
        dict: _description_
    """    
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
    """Validate a key=value pair, where key is in dot notation. i.e. a.b.c=value1 d=value2

    Args:
        pair (str): A key=value pair.

    Returns:
        bool: True if the pair is valid, False otherwise.
    """    
    if match(r'^[a-zA-Z0-9_\.]+=[^\[\]]+$', pair):
        return True

    return False

def validate_key_value_lst(pair: str) -> bool:
    """Validate a key=value pair, where value is a list of values. i.e. a.b.c=[a,b,d] d=[1,2,a,c]

    Args:
        pair (str): A key=value pair.

    Returns:
        bool: True if the pair is valid, False otherwise.
    """    
    if match(r'^[a-zA-Z0-9_\.]+=\[[^\]]*]+$', pair):
        return True

    return False