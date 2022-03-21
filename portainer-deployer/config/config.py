import configparser
from os import path

class ConfigManager:
    """Class to manage config files.
    """    
    def __init__(self, path_to_config_file: str, default_section: str = None) -> None:
        """Initialize the ConfigManager class.

        Args:
            path_to_config_file (str): Path to the config file to manage.
            default_section (str, optional): default section to take config into the file. Defaults to None.
        """       

        # Validate path
        if path.isfile(path_to_config_file):
            self._path_to_config_file = path_to_config_file 

        else:
            raise FileNotFoundError(f"{path_to_config_file} does not exist or is not a file.")
        
        if default_section:
            self.section = default_section
        else:
            self._section = default_section

    # ============== Setters & Getters ==============
    @property
    def section(self) -> str:
        """Get the current section.

        Returns:
            str: Current section.
        """        
        return self._section

    @section.setter
    def section(self, section: str) -> None:
        """Set the current section.

        Args:
            section (str): Section to set.
        """        
        self._section = section
        self.__dict__.update(self.get_section_config(section))


    # ============== decorators ==============
    def _use_default_section(func):
        """Decorator to pass the default section to the function.

        Args:
            func (func): Function to decorate.
        """        
        def inner(self, *args, **kwargs):
            if self.section is None:    
                return func(self, *args, **kwargs)
            
            return func(self, *args, **kwargs, section=self.section)
        return inner


    # ============== Public Methods ==============
    def reset_section(self) -> None:
        """Reset the section to the default section value (None).
        """        
        self.section = None

    @_use_default_section
    def set_var(self, key: str, new_value: str, section: str) -> bool:
        """Set a value in the config file.

        Args:
            section (str): Section to set the value in.
            key (str): Key to set the value. 
            value (str): Value to set. 

        Raises:
            configparser.Error: If the section does not exist. 

        Returns:
            bool: True if the value was set, False otherwise. 
        """
        try:
            config = configparser.ConfigParser()
            config.read(self._path_to_config_file)
            config[section.upper()][key] = new_value
            with open(self._path_to_config_file, 'w') as configfile:
                config.write(configfile)
            return True

        except configparser.Error as e:
            raise configparser.Error(f"Error: {e}")


    @_use_default_section
    def get_var(self, key: str, section: str) -> str:
        """ Get a value from the config file.

        Args:
            section (str): Section to get the value from. 
            key (str): Key to get the value. 

        Raises:
            configparser.Error: If the section does not exist. 

        Returns:
            str: Value of the key. 
        """
        try:
            config = configparser.ConfigParser()
            config.read(self._path_to_config_file)
            return config[section.upper()][key]

        except configparser.Error as e:
            raise configparser.Error(f"Error: {e}")


    @_use_default_section
    def get_boolean_var(self, key: str, section: str) -> bool:
        """ Get a boolean value from the config file.

        Args:
            section (str): Section to get the value from. 
            key (str): Key to get the value. 

        Raises:
            configparser.Error: If the section does not exist. 

        Returns:
            bool: Boolean value of the key. 
        """
        try:
            config = configparser.ConfigParser()
            config.read(self._path_to_config_file)
            return config.getboolean(section, key)

        except configparser.Error as e:
            raise configparser.Error(f"Error: {e}")

    def get_section_config(self, section: str) -> dict:
        """Get a section config.

        Args:
            section (str): Section to get the config from. 

        Raises:
            configparser.Error: If the section does not exist. 

        Returns:
            dict: Section config. 
        """
        try:
            config = configparser.ConfigParser()
            config.read(self._path_to_config_file)
            return dict(config[section])

        except configparser.Error as e:
            raise configparser.Error(f"Error: {e}")

