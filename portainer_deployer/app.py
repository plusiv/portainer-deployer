import argparse
import sys
import os
from urllib import response
import requests
from json import loads
from urllib3.exceptions import InsecureRequestWarning
from utils.utils import edit_yml_file, format_stack_info, format_stack_info_generator, generate_random_hash, validate_key_value, validate_key_value_lst, generate_response 
from config.config import ConfigManager

class PortainerAPIConsumer:
    """Class to manage the Portainer API
    """    
    def __init__(self, api_config_path: str) -> None:
        PATH_TO_CONFIG = api_config_path

        # Load config
        self._portainer_config = ConfigManager(PATH_TO_CONFIG, default_section='PORTAINER')

        # Set non-ssl connection
        self.use_ssl = self._portainer_config.get_boolean_var('SSL')
        if not self.use_ssl and self._portainer_config.url.split('://')[0] == 'https':
            # Suppress only the single warning from urllib3 needed.
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

        # Set portainer connection parameters
        self.__portainer_connection_str = f"{self._portainer_config.url}:{self._portainer_config.port}" 
        self.__connection_headers = {'X-API-Key': self._portainer_config.token}


    def get_stack(self, name:str=None, stack_id:int=None) -> dict:
        """Get a stack from portainer

        Args:
            name (str, optional): Name of the stack in Portainer. Defaults to None.
            stack_id (int, optional): Id of the stack in Portainer. Defaults to None.

        Returns:
            dict: Dictionary with the status and detail of the operation.
        """
        spacing_str = '{0:<5} {1:<12} {2:<30} {3:30} {4:<30}'

        try:
            if stack_id:
                    r = requests.get(
                        f"{self.__portainer_connection_str}/api/stacks/{stack_id}", 
                        headers=self.__connection_headers,
                        verify=self.use_ssl
                    )
                    
                    r.raise_for_status()
                    data = format_stack_info(r.json())

                    print(spacing_str.format('Id', 'Endpoint Id', 'Name', 'Creation', 'Last Updated'))
                    print(spacing_str.format(*data))

            elif name:
                r = requests.get(
                    f"{self.__portainer_connection_str}/api/stacks", 
                    headers=self.__connection_headers,
                    verify=self.use_ssl
                )
                
                r.raise_for_status()
                data = format_stack_info_generator(r.json())

                print(spacing_str.format('Id', 'Endpoint Id', 'Name', 'Creation', 'Last Updated'))
                for stack in data:
                    if stack[2] == name:
                        print(spacing_str.format(*stack))
                        break 
                else:
                    raise Exception(f"Stack {name} not found in the database.")

            else:
                r = requests.get(
                    f"{self.__portainer_connection_str}/api/stacks", 
                    headers=self.__connection_headers,
                    verify=self.use_ssl
                )
                
                r.raise_for_status()
                data = format_stack_info_generator(r.json())

                print(spacing_str.format('Id', 'Endpoint Id', 'Name', 'Creation', 'Last Updated'))
                for stack in data:
                    print(spacing_str.format(*stack))

            return generate_response('Stack(s) pulled successfully', status=True, code=r.status_code)

        except requests.HTTPError as e:
            return generate_response(e.response.json()['message'], e.response.json()['details'], code=e.response.status_code)
        
        except requests.exceptions.RequestException as e:
            return generate_response(e.response.json()['message'], e.response.json()['details'], code=e.response.status_code) 
        
        except Exception as e:
            return generate_response(str(e), code=500)


    def post_stack_from_str(self, stack: str, endpoint_id: int, name: str = generate_random_hash()):
       #TODO: Implement
       pass


    def post_stack_from_file(self, path: str, endpoint_id: int, name: str) -> dict:
        """Post a stack from a file.

        Args:
            path (str): Path to the file.
            endpoint_id (int): Id of the endpoint in Portainer.
            name (str): Name of the stack in Portainer.

        Returns:
            dict: Dictionary with the status and detail of the operation.
        """        
        try:
            name = name if name else generate_random_hash()
            
            # Open file
            with open(path, 'r') as f:
                form_data = {
                    'Name': name 
                }
                
                params = {
                    "type": 2,
                    "endpointId": endpoint_id,
                    "method": "file"
                }
                
                response = requests.post(self.__portainer_connection_str + '/api/stacks',
                    data=form_data, 
                    params=params,
                    files={'file': f},
                    headers=self.__connection_headers, 
                    verify=self.use_ssl
                )

                return generate_response(f'Stack {name} from {path} posted successfully under the endpoint {endpoint_id}.', status=True, code=response.status_code)
                
        except requests.HTTPError as e:
            return generate_response(e.response.json()['message'], e.response.json()['details'], code=e.response.status_code)
        
        except requests.exceptions.RequestException as e:
            return generate_response(e.response.json()['message'], e.response.json()['details'], code=e.response.status_code)
        
        except FileNotFoundError as e:
            return generate_response(f'File {path} not found.', code=None)
        
        except Exception as e:
            return generate_response(str(e), None)


    def update_stack(self, stack_id: str, stack: str):
        #TODO: Implement
        pass


class PortainerDeployer:
    """Manage Portainer's Stacks usgin its API throught Command Line.
    """
    def __init__(self) -> None:
        """Initialize the PortainerDeployer class and runs the main function.
        """        

        # Load .env file
        env_file = ConfigManager('.env', default_section='CONFIG')
        self.PATH_TO_CONFIG = env_file.path_to_config

        # Set API consummer object
        self.api_consumer = PortainerAPIConsumer(api_config_path=self.PATH_TO_CONFIG)

        self.parser = self.__parser()
        

    def run(self):
        """Run the main function.
        """        
        # Set arguments
        self.parser = self.__parser()
        parser_args = self.parser.parse_args(args=None if len(sys.argv) > 2 else [sys.argv[1], '-h'] if len(sys.argv) == 2 else ['-h'])
        
        response = parser_args.func(parser_args)

        if response['status']:
            # Exits with success
            sys.exit(0)
        else:
            self._error_handler(response['message'], response['details'])


    def __parser(self) -> argparse.ArgumentParser:
        """Parse and handle given arguments.

        Returns:
            parser (argparse.ArgumentParser): Main parser.
        """

        parser = argparse.ArgumentParser(
            description='Deploy stacks to portainer',
            prog='portainerDeployer'
        )
        
        parser.add_argument('--version', action='version', version='%(prog)s 0.0.1 (Alpha)')
        subparsers = parser.add_subparsers(help='Sub-commands for actions', dest='subparser_name')

        
        # ========================== Sub-commands for get ==========================
        parser_get = subparsers.add_parser('get', 
            help='Help for action Get', 
            description='Get a stack info from portainer.'
        )
        
        # Mutually exclusive arguments for --name and --id
        mutually_exclusive_name_id = parser_get.add_mutually_exclusive_group()

        mutually_exclusive_name_id.add_argument('--id',
            action='store',
            help="Id for the stack when set action to 'get'",          
            type=int
        )

        mutually_exclusive_name_id.add_argument('--name',
            '-n',
            action='store',
            help="Name of the stack to look for",   
            type=str
        )


        mutually_exclusive_name_id.add_argument('--all',
            '-a',
            action='store_true',
            help="Gets all stacks in portainer",   
        )

        parser_get.set_defaults(func=self._get_sub_command)


        # ========================== Sub-commands for deploy ==========================
        parser_deploy = subparsers.add_parser('deploy', help='Help for action Deploy')

        mutually_exclusive_stack_path = parser_deploy.add_mutually_exclusive_group()

        mutually_exclusive_stack_path.add_argument('--stack',
            type=str, 
            help="Docker Compose string for the satack",
            nargs='?',
            default=(None if sys.stdin.isatty() else sys.stdin))

        
        mutually_exclusive_stack_path.add_argument('--path',
            '-p',
            action='store',
            type=str,
            help='The path to Docker Compose file for the stack',
            required=False,
            default=None)

        parser_deploy.add_argument('--name',
            '-n',
            action='store',
            help="Name of the stack to look for",
        )
        
        parser_deploy.add_argument('--update-keys', 
            '-u',
            action='extend', 
            type=str,
            nargs='+',
            help='Modify the stack file/string by passing a list of key=value pairs, where the key is in dot notation. i.e. a.b.c=value1 d=value2',
        )


        parser_deploy.add_argument('--endpoint', 
            '-e',
            action='store',
            type=int,
            help='Endponint Id in Portainer'
        )


        parser_deploy.set_defaults(func=self._deploy_sub_command)


        # ========================== Sub-commands for config ==========================
        parser_config = subparsers.add_parser('config', help='Help for Config sub-command')
        
        mutually_exclusive_config = parser_config.add_mutually_exclusive_group() 

        mutually_exclusive_config.add_argument('--set',
            '-s',
            action='extend',
            nargs='+',
            type=str,
            help='Set a config value')

        mutually_exclusive_config.add_argument('--get',
            '-g',
            action='store',
            type=str,
            help='Get a config value')

        parser_config.set_defaults(func=self._config_sub_command)
 
        return parser
        

    def _error_handler(self, error_message: str, error_detail: str) -> None: 
        """Prints an error message and exits with error code.

        Args:
            error_message (str): Error message to be printed.
            error_code (int, optional): Error code to be used. Defaults to None.
        """        
        self.parser.error(error_detail)


    def _config_sub_command(self, args) -> dict:
        """Config sub-command.

        Args:
            args (argparse.Namespace): Parsed arguments.
        """

        config = ConfigManager(self.PATH_TO_CONFIG)
        if args.set:
            for pair in args.set:
                splited = pair.split('=')
                if len(splited) != 2:
                    return generate_response(f'Invalid config pair: {pair}')
                
                value = splited[1]
                section_key = splited[0].split('.')
                if len(section_key) != 2:
                    return generate_response(f'Invalid config pair: {pair}')
                section, key = section_key  
                config.set_var(key=key, new_value=value, section=section)

            print(f'Config updated for: {args.set}')

        elif args.get:
            pair = args.get
            splited = pair.split('.')
            if len(splited) != 2:
                    return generate_response(f'Invalid config pair: {pair}')
            
            section,key = splited
            print(config.get_var(key=key, section=section))
           
        else:
            return generate_response('No config action specified')

        return generate_response(f'Config operation {"get" if args.get else "set"} completed successfully', status=True)


    def _get_sub_command(self , args: argparse.Namespace) -> dict:
        """Get sub-command default function. Excutes get functions according given arguments.

        Args:
            args (argparse.Namespace): Parsed arguments. 
        """        

        if args.all:
            response = self.api_consumer.get_stack()
        else:
            response = self.api_consumer.get_stack(name=args.name, stack_id=args.id)

        return response
        

    def _deploy_sub_command(self, args: argparse.Namespace) -> dict:
        """Deploy sub-command default function. Excutes deploy functions according given arguments.

        Args:
            args (argparse.Namespace): Parsed arguments. 
        """

        # Validate endpoint set
        if args.endpoint is None:
            return generate_response('Endpoint not set', 'Endpoint not set. Please set the endpoint id with --endpoint')

        if args.stack:
            if args.update_keys:
                return generate_response('Invalid use of --update-keys', 'You can not use "--update-keys" argument with "--stack" argument. It is only available for "--path" argument.')
            response = self.api_consumer.post_stack_from_str(stack=args.stack, endpoint_id=args.endpoint)
        
        elif args.path:
            if not os.path.isfile(args.path):
                return generate_response(f'Invalid path to Docker Compose file: {args.path}')

            if args.update_keys:
                for pair in args.update_keys:
                    if validate_key_value(pair=pair):
                        keys, new_value = pair.split('=')
                        edited = edit_yml_file(path=args.path, key_group=keys, new_value=new_value)
                        if edited:
                            return generate_response(edited)
                    
                    elif validate_key_value_lst(pair=pair):
                        keys, new_value = pair.split('=')
                        edited = edit_yml_file(path=args.path, key_group=keys, new_value=new_value[1:-1].split(','))
                        if edited:
                            return generate_response(edited)

                    else:
                        return generate_response(f'Invalid key=value pair in --update-keys argument: {pair}')

            response = self.api_consumer.post_stack_from_file(path=args.path, name=args.name, endpoint_id=args.endpoint)

        return response


if __name__ == '__main__':
    PortainerDeployer().run()