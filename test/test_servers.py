"""
Unittests for the rpc.servers module
"""
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from rpc import exceptions, servers

# Use this as our dummy handler
class Handler(object):
    def ping(self):
        return "pong!"

    def sayhi(self, person):
        return "Hi " + person

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


class HTTPServerTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_bind_twice(self):
        """ Bind and serve our instance"""
        s1 = servers.HTTPServer("localhost", 8878, Handler)
        with self.assertRaises(exceptions.PortInUseError):
            servers.HTTPServer("localhost", 8878, Handler)


    def tearDown(self):
        pass



if __name__ == '__main__':
    unittest.main()
