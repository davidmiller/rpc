"""
Unittests for the rpc.ini module
"""
import ConfigParser
import StringIO
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from mock import MagicMock

from rpc import ini

SAMPLEINI = """
[section]
option=foo
goo=3
"""

class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        self.conf = StringIO.StringIO(SAMPLEINI)
        self.ini = ini.IniFile(self.conf)

    def test_config(self):
        """ Can we initialize our config?"""
        self.assertEqual('unknown', self.ini._basename)
        self.assertIsInstance(self.ini._config, ConfigParser.ConfigParser)

    def test_repr(self):
        """ What should we print?"""
        mock_filelike = MagicMock(name="Mock File-like")
        mock_filelike.name = "/tmp/slash/fubar.conf"
        mock_filelike.readline.return_value = ''
        config = ini.IniFile(mock_filelike)
        expected = "<IniFile fubar.conf>"
        self.assertEqual(expected, str(config))

    def test_get_nodefault(self):
        "Raise when no default given"
        with self.assertRaises(ConfigParser.NoOptionError):
            self.ini.get("section", "FTW")
        with self.assertRaises(ConfigParser.NoSectionError):
            self.ini.get("FTW", "Larry?")

    def test_get_nooption(self):
        """  Fail gracefully if the INIfile has no option"""
        self.assertEqual("HERE", self.ini.get("section", "where", "HERE"))



if __name__ == '__main__':
    unittest.main()

