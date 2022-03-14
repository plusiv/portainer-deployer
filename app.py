import argparse
import configparser
import sys
import os
import requests
from urllib3.exceptions import InsecureRequestWarning
from utils.utils import *


class PortainerDeployer:
    """Manage Portainer's Stacks usgin its API.
    """
    def __init__(self):
        """Initialize the PortainerDeployer class and runs the main function.
        """        
        # Load .env file
        env_file = configparser.ConfigParser()
        env_file.read('.env')
        PATH_TO_CONFIG = env_file['CONFIG']['PATH_TO_CONFIG']

        # Load config
        config = configparser.ConfigParser()
        config.read(PATH_TO_CONFIG)
        self.portainer_config = config['PORTAINER']

        # Set non-ssl connection
        if not self.portainer_config.getboolean('SSL') and self.portainer_config['URL'].split('://')[0] == 'https':
            # Suppress only the single warning from urllib3 needed.
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

        # Set portainer connection
        self.portainer_connection = f"{self.portainer_config['URL']}:{self.portainer_config['PORT']}" 
        self.connection_headers = {'X-API-Key': self.portainer_config['TOKEN']}
        
        # Set arguments
        self.args = self.parse_args()

        # Run main function
        self.main()
        

    @staticmethod
    def parse_args() -> argparse.Namespace:
        """Parse arguments from the command line.

        Returns:
            argparse.Namespace: Args parsed from the command line.
        """        
        
        parser = argparse.ArgumentParser(
            description='Deploy stacks to portainer',
            prog='portainerDeployer'
        )
        
        parser.add_argument('action',
            metavar='action',
            action='store',
            choices=['get', 'deploy', 'redeploy'],
            help='Action to be executed with the stack. It allows: get, deploy, redeploy',
            type=str)

        parser.add_argument('--stack',
            type=str, 
            help="Docker Compose string for the satack",
            nargs='?',
            default=(None if sys.stdin.isatty() else sys.stdin))


        parser.add_argument('--path',
            '-p',
            action='store',
            type=str,
            help='The path to Docker Compose file for the stack',
            required=False,
            default=None)

        # Mutually exclusive arguments for --name and --id
        mutually_exclusive_name_id = parser.add_mutually_exclusive_group()

        mutually_exclusive_name_id.add_argument('--id',
            action='store',
            help="Id for the stack when set action to 'get'",          
            type=int
        )

        mutually_exclusive_name_id.add_argument('--name',
            '-n',
            action='store',
            help="Name for the stack when action is set to 'get' or 'deploy'",   
            type=str
        )
        
        parser.add_argument('--modify-stack', 
            '-m',
            action='extend', 
            type=str,
            nargs='*',
            help='Modify the stack file/string by passing a list of key=value pairs, where the key is in dot notation. i.e. a.b.c=value1 d=value2',
        )


        parser.add_argument('--endpoint', 
            '-e',
            action='store',
            type=int,
            help='Endponint Id in Portainer'
        )
        

        parser.add_argument('--version', action='version', version='%(prog)s 0.0.1 (Alpha)')

        args = parser.parse_args()

        """"Some validations"""
        # Validate "action" is set to "get" when using "id" or "name" arguments 
        if args.id or args.name:
            if args.action != 'get':
                parser.error('The arguments "id" and/or "name" must be set with the parameter "action" set as "get"') 

        if args.modify_stack:
            if args.action != 'deploy':
                parser.error('The argument "--modify-stack" must be set with the parameter "action" set as "deploy"')
            
            if validate_key_value(args.modify_stack):
                parser.error('There is something wrong with the value(s) of "--modify-stack" argument. Please make sure it follows the syntax key=value.')

        # Validate "action" is set to "deploy" when using "path"  or "stack" arguments
        if args.action == 'deploy' and not args.stack and not args.path:
            parser.error('You did not provided a Path or Stack string, please read the help instruct in order to perform this action.')

            if args.path and os.path.isfile(args.path):
                parser.error('The specified file does not exist.')
        
        return args


    def get_stack(self, name:str=None, stack_id:int=None):
        """_summary_: Get a stack from portainer

        Args:
            name (str, optional): Name of the stack in Portainer. Defaults to None.
            stack_id (int, optional): Id of the stack in Portainer. Defaults to None.
        """
        r = requests.get(
            f"{self.portainer_connection}/api/stacks", 
            headers=self.connection_headers,
            verify=False
        )
        data = r.json()

        spacing_str = '{0:<5} {1:<12} {2:<30} {3:30} {4:<30}'
        print(spacing_str.format('Id', 'Endpoint Id', 'Name', 'Creation', 'Last Updated'))

        data = format_stack_list(data)
        
        # Return all stacks if name and id aren't set
        if not name and not stack_id:
            for stack in data:
                print(spacing_str.format(*stack))
        
        # Return a specific stack given by the name
        elif name and not stack_id:
            for stack in data:
                if stack[2] == name:
                    print(spacing_str.format(*stack))
        
        # Return a specific stack given by the stack id
        else:
            for stack in data:
                if stack[0] == stack_id:
                    print(spacing_str.format(*stack))


    def post_stack(self, stack: str):
       pass

    def post_stack_from_file(self, path: str):
        # Open file
        with open(path, 'r') as f:
            form_data = {
                'Name': self.args.name if self.args.name else generate_random_hash()
            }
            params = {
                "type": 2,
                "endpointId": 2,
                "method": "file"
            }
            r = requests.post(self.portainer_connection + '/api/stacks',
                 data=form_data, 
                 params=params,
                 files={'file': f},
                 headers=self.connection_headers, 
                 verify=False
            )
            print(r.status_code, r.text)
    
    def update_stack(self, stack_id: str, stack: str):
        pass

    def main(self):
        args = self.args
        
        if args.action == 'get':
            self.get_stack(name=args.name, stack_id=args.id)
        
        elif args.action == 'deploy':
            # Validate just one of the arguments is set
            
            
            if args.path:
                if not os.path.exists(args.path):
                    sys.exit('Error: The specified file does not exist.')

                self.post_stack_from_file(args.path)
            else:
                self.post_stack(stack=args.stack)

if __name__ == '__main__':
    PortainerDeployer()