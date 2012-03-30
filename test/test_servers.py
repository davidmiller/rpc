"""
Unittests for the rpc.servers module
"""
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from rpc import servers

class ServerTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_initialise(self):
        """ Can we initialise?"""
        server = servers.Server(host="localhost", port=6786, handler=dict)
        self.assertEqual("localhost", server.host)
        self.assertEqual(6786, server.port)
        self.assertIsInstance(server.handler, dict)

    def test_scaffold(self):
        """
        Should be a no-op
        """
        server = servers.Server(host="localhost", port=6786, handler=dict)
        self.assertEqual(None, server.scaffold())

    def test_serve_raises(self):
        """ Dummy serve() should raise """
        server = servers.Server(host="localhost", port=6786, handler=dict)
        with self.assertRaises(NotImplementedError):
            server.serve()

    def tearDown(self):
        pass



if __name__ == '__main__':
    unittest.main()
