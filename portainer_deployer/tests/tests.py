import unittest
from app import PortainerDeployer

class PortinaerCMDTest(unittest.TestCase):

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

    def test_get_subcommand(self):
        tester = PortainerDeployer()
        args = tester.parser.parse_args(['get'])
        print(vars(args))

        #self.assertEqual(cm.exception.code, 0)

if __name__ == '__main__':
    unittest.main()