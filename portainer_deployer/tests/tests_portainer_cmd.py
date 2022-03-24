import unittest
from unittest.mock import Mock, MagicMock


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
        tester = PortainerDeployer()
        args = tester.parser.parse_args(['deploy'])

        self.assertEqual(args.func, tester._deploy_sub_command)
    
    def test_config_subcommand(self):
        tester = PortainerDeployer()
        args = tester.parser.parse_args(['config'])

        self.assertEqual(args.func, tester._config_sub_command)
    
    # ================================ Test API Consumer ================================
    def test_get_all_stacks(self):
        tester = PortainerDeployerTest()
        args = tester.parser.parse_args(['get', '--all'])
        args.func(args)
        tester.api_consumer.get_stack.assert_called_once()

    def test_get_stack(self):
        tester = PortainerDeployerTest()
        args = tester.parser.parse_args(['get', '--all'])
        args.func(args)
        tester.api_consumer.get_stack.assert_called_once()

if __name__ == '__main__':
    unittest.main()