import unittest
from unittest.mock import Mock, MagicMock
from random import randint


from app import PortainerDeployer
from utils.utils import generate_response

class PortainerDeployerTest(PortainerDeployer):
    def __init__(self):
        super().__init__()
        self.create_api_consumer_mock() 

    def create_api_consumer_mock(self):
        self.api_consumer = Mock()


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
        self.assertEquals(args.func(args), generated_response)

        # Assert error handling
        tester = self.tester
        stack_id = 23 # Unexisting stack id

        cmd_args = ['get', '--id', str(stack_id)]
        generated_response = generate_response('Not found in database', status=False, code=404)
        tester.api_consumer.get_stack.return_value = generated_response 
        args = tester.parser.parse_args(cmd_args)
        
        self.assertEquals(args.func(args), generated_response)        


    def test_get_stack_by_name(self):
        tester = self.tester
        stack_name = 'fake_stack_name'
        cmd_args = ['get', '--name', stack_name]
        generated_response = generate_response('ok', status=True, code=None)
        tester.api_consumer.get_stack.return_value = generated_response 
        
        args = tester.parser.parse_args(cmd_args)
        args.func(args)
        
        tester.api_consumer.get_stack.assert_called_once_with(name=stack_name, stack_id=None)
        self.assertEquals(args.func(args), generated_response)

        # Assert error handling
        tester = self.tester
        stack_name = 'another_fake_name' # Unexisting stack id

        cmd_args = ['get', '--name', stack_name] 
        generated_response = generate_response('Not found in database', status=False, code=404)
        tester.api_consumer.get_stack.return_value = generated_response 
        args = tester.parser.parse_args(cmd_args)
        
        self.assertEquals(args.func(args), generated_response)        

        

if __name__ == '__main__':
    unittest.main()