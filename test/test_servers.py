"""
Unittests for the rpc.servers module
"""
import unittest

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

    def test_serve_raises(self):
        """ Dummy serve() should raise """
        server = servers.Server(host="localhost", port=6786, handler=dict)
        with self.assertRaises(NotImplementedError):
            server.serve()

    def tearDown(self):
        pass



if __name__ == '__main__':
    unittest.main()
