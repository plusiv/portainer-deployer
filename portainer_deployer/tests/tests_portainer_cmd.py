import unittest
from unittest.mock import Mock, MagicMock
from random import randint


from app import PortainerDeployer


class PortainerDeployerTest(PortainerDeployer):
    def __init__(self):
        super().__init__()
        self.create_api_consumer_mock() 

    def create_api_consumer_mock(self):
        self.api_consumer = Mock()


class PortainerCMDTest(unittest.TestCase):
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
        tester = PortainerDeployerTest()
        args = tester.parser.parse_args(['get', '--all'])
        args.func(args)
        tester.api_consumer.get_stack.assert_called_once()

    def test_get_stack_by_id(self):
        tester = PortainerDeployerTest()

        stack_id = randint(1, 100)
        cmd_args = ['get', '--id', str(stack_id)]
        
        args = tester.parser.parse_args(cmd_args)
        args.func(args)
        tester.api_consumer.get_stack.assert_called_once_with(name=None, stack_id=stack_id)

    def test_get_stack_by_name(self):
        tester = PortainerDeployerTest()

        stack_name = 'random_stack_name'
        cmd_args = ['get', '--name', stack_name]
        
        args = tester.parser.parse_args(cmd_args)
        args.func(args)
        tester.api_consumer.get_stack.assert_called_once_with(name=stack_name, stack_id=None)
        

if __name__ == '__main__':
    unittest.main()