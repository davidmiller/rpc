"""
Unittests for the xmlrpc module
"""
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from mock import Mock

from rpc import xmlrpc

class XmlClientTestCase(unittest.TestCase):
    def setUp(self):
        self.c = xmlrpc.Client('http://localhost/xmlrpc')

    def test_repr(self):
        """ Do we sting nicely?"""
        expected = '<XML RPC Client for http://localhost/xmlrpc>'
        self.assertEqual(expected, str(self.c))

    def test_apicall(self):
        """ Make the call to the XML RPC Proxy """
        mock_proxy = Mock(name='Mock PRoxy')



    def tearDown(self):
        pass



if __name__ == '__main__':
    unittest.main()
