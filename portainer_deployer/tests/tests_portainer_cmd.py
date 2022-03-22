import unittest
from app import PortainerDeployer

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

if __name__ == '__main__':
    unittest.main()