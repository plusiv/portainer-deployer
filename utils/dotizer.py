
class Dotizer:
    """Maps curly braces to dot notation for dictionaries"""
    def __init__(self, dict_obj:dict):
        self.__dict__.update(dict_obj)

    def __getattribute__(self, name):
        if name == '__dict__':
            return super().__getattribute__(name)

        if isinstance(super().__getattribute__(name), dict):
            return Dotizer(**super().__getattribute__(name))
        
        else:
            return super().__getattribute__(name)