import unittest
from unittest.mock import Mock
from random import randint
from portainer_deployer.app import PortainerDeployer
from portainer_deployer.utils import generate_response

class PortainerDeployerTest(PortainerDeployer):
    def __init__(self):
        super().__init__()
        self._api_consumer = Mock()

    # Prevent decorator modifies Mock of self.api_consumer
    @property
    def api_consumer(self):
        return self._api_consumer
    
    @api_consumer.setter
    def api_consumer(self, value):
        ...


class PortainerCMDTest(unittest.TestCase):
    @property
    def tester(self):
        return PortainerDeployerTest()    


    # ================================ Test Defualt functions in sub-commands ================================
    def test_get_subcommand(self):
        tester = PortainerDeployerTest()
        args = tester.parser.parse_args(['get'])
        self.assertEqual(args.func, tester._get_sub_command)

    def test_deploy_subcommand(self):
        tester = PortainerDeployerTest()
        args = tester.parser.parse_args(['deploy'])

        self.assertEqual(args.func, tester._deploy_sub_command)

    def test_config_subcommand(self):
        tester = PortainerDeployerTest()
        args = tester.parser.parse_args(['config'])

        self.assertEqual(args.func, tester._config_sub_command)
    
    # ================================ Test API Consumer ================================
    def test_get_all_stacks(self):
        # Assert Get all Stacks
        tester = self.tester
        args = tester.parser.parse_args(['get', '--all'])
        args.func(args)
        tester.api_consumer.get_stack.assert_called_once()

    def test_get_stack_by_id(self):
        tester = self.tester
        stack_id = randint(1, 100)
        cmd_args = ['get', '--id', str(stack_id)]
        generated_response = generate_response('ok', status=True, code=None)
        tester.api_consumer.get_stack.return_value = generated_response 
        
        args = tester.parser.parse_args(cmd_args)
        args.func(args)
        
        tester.api_consumer.get_stack.assert_called_once_with(name=None, stack_id=stack_id)
        self.assertEqual(args.func(args), generated_response)

        # Assert error handling
        tester = self.tester
        stack_id = 23 # Unexisting stack id

        cmd_args = ['get', '--id', str(stack_id)]
        generated_response = generate_response('Not found in database', status=False, code=404)
        tester.api_consumer.get_stack.return_value = generated_response 
        args = tester.parser.parse_args(cmd_args)
        
        self.assertEqual(args.func(args), generated_response)        


    def test_get_stack_by_name(self):
        tester = self.tester
        generated_response = generate_response('ok', status=True, code=None)
        tester.api_consumer.get_stack.return_value = generated_response 
        stack_name = 'fake_stack_name'
        cmd_args = ['get', '--name', stack_name]
        
        args = tester.parser.parse_args(cmd_args)
        args.func(args)
        
        tester.api_consumer.get_stack.assert_called_once_with(name=stack_name, stack_id=None)
        self.assertEqual(args.func(args), generated_response)

        # Assert error handling
        tester = self.tester
        generated_response = generate_response('Not found in database', status=False, code=404)
        tester.api_consumer.get_stack.return_value = generated_response 
        stack_name = 'another_fake_name' # Unexisting stack id

        cmd_args = ['get', '--name', stack_name] 
        args = tester.parser.parse_args(cmd_args)
        
        self.assertEqual(args.func(args), generated_response)        

        
    def test_deploy_stack_by_stdin(self):
        tester = self.tester
        generated_response = generate_response('ok', status=True, code=None)
        tester.api_consumer.post_stack_from_file.return_value = generated_response
        path, endpoint, name = ('/test/path/to/file', 1, 'test_stack')
        example_stack = "version: 3\n services:\n web:\n image:nginx"
        cmd_args = ['deploy', '--endpoint', str(endpoint), '--name', name, example_stack]
        args = tester.parser.parse_args(cmd_args)
        args.func(args)
        tester.api_consumer.post_stack_from_str.assert_called_once_with(stack=example_stack, name=name, endpoint_id=endpoint)

        # Assert error handling
        tester = self.tester
        generated_response = generate_response('error', status=False, code=None) 
        tester.api_consumer.post_stack_from_str.return_value = generated_response
        cmd_args = ['deploy', '--endpoint', str(endpoint), '--name', name, 'wrong_stack']
        args = tester.parser.parse_args(cmd_args)
        self.assertEqual(args.func(args), generated_response)


    def test_deploy_stack_by_path(self):
        tester = self.tester
        generated_response = generate_response('ok', status=True, code=None)
        tester.api_consumer.post_stack_from_file.return_value = generated_response
        path, endpoint, name = ('/test/path/to/file', 1, 'test_stack')
        
        cmd_args = ['deploy', '--path', path, '--endpoint', str(endpoint), '--name', name]
        args = tester.parser.parse_args(cmd_args)
        args.func(args)
        tester.api_consumer.post_stack_from_file.assert_called_once_with(path=path, name=name, endpoint_id=endpoint)

        # Assert error handling
        tester = self.tester
        generated_response = generate_response('error', status=False, code=500)
        tester.api_consumer.post_stack_from_file.return_value = generated_response
        args = tester.parser.parse_args(cmd_args)
        response = args.func(args)
        self.assertEqual(response, generated_response)
        

if __name__ == '__main__':
    unittest.main()