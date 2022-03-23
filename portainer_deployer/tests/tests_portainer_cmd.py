import unittest
from unittest.mock import Mock
from app import PortainerDeployer


class PortainerDeployerTest(PortainerDeployer):
    def __init__(self):
        super().__init__()
        
        self.create_api_consumer_mock() 

    def create_api_consumer_mock(self):
        self.api_consumer = Mock()


class PortainerCMDTest(unittest.TestCase):

    # ================================ Test Helps ================================
    def test_global_help(self):
        tester = PortainerDeployer()
        with self.assertRaises(SystemExit) as cm:
            tester.parser.parse_args(['--help'])

        self.assertEqual(cm.exception.code, 0)

        
    def test_get_help(self):
        tester = PortainerDeployer()
        with self.assertRaises(SystemExit) as cm:
            tester.parser.parse_args(['get', '--help'])

        self.assertEqual(cm.exception.code, 0)


    def test_deploy_help(self):
        tester = PortainerDeployer()
        with self.assertRaises(SystemExit) as cm:
            tester.parser.parse_args(['deploy', '--help'])

        self.assertEqual(cm.exception.code, 0)


    def test_config_help(self):
        tester = PortainerDeployer()
        with self.assertRaises(SystemExit) as cm:
            tester.parser.parse_args(['config', '--help'])

        self.assertEqual(cm.exception.code, 0)


    # ================================ Test Defualt functions in sub-commands ================================

    def test_get_subcommand(self):
        tester = PortainerDeployer()
        args = tester.parser.parse_args(['get'])

        self.assertEqual(args.func.__name__, '__get_sub_command')

    def test_deploy_subcommand(self):
        tester = PortainerDeployer()
        args = tester.parser.parse_args(['deploy'])

        self.assertEqual(args.func.__name__, '__deploy_sub_command')
    
    def test_config_subcommand(self):
        tester = PortainerDeployer()
        args = tester.parser.parse_args(['config'])

        self.assertEqual(args.func.__name__, '__config_sub_command')
    
    # ================================ Test API Consumer ================================
    def test_get_stack(self):
        pass

if __name__ == '__main__':
    unittest.main()