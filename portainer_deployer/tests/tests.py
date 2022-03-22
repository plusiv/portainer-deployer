import unittest
from app import PortainerDeployerTest

class PortinaerCMDTest(unittest.TestCase):


    def test_portinaer_cmd_help(self):
        tester = PortainerDeployerTest()
        with self.assertRaises(SystemExit) as cm:
            tester.parser.parse_args(['--help'])

        self.assertEqual(cm.exception.code, 0)


if __name__ == '__main__':
    unittest.main()