"""
Unittests for the rpc.jsonrpc module
"""
import unittest

from rpc import jsonrpc

class ChainTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_chain(self):
        """ Chain JSON RPC Clients"""
        one, two = jsonrpc.chain("localhost").chain("example.com")
        self.assertEqual(one.url, "localhost")
        self.assertEqual(two.url, "example.com")

    def tearDown(self):
        pass



if __name__ == '__main__':
    unittest.main()
