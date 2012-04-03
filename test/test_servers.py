"""
Unittests for the rpc.servers module
"""
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from mock import Mock

from rpc import servers

# Use this as our dummy handler
class Handler(object):
    def ping(self):
        return "pong!"

    def sayhi(self, person):
        return "Hi " + person

class ServerTestCase(unittest.TestCase):
    def setUp(self):
        self.s = servers.Server(host="localhost", port=6786, handler=Handler)

    def test_initialise(self):
        """ Can we initialise?"""
        server = servers.Server(host="localhost", port=6786, handler=dict)
        self.assertEqual("localhost", server.host)
        self.assertEqual(6786, server.port)
        self.assertIsInstance(server.handler, dict)

    def test_close(self):
        """ Should be a noop """
        self.assertEqual(None, self.s.close())

    def test_scaffold(self):
        """
        Should be a no-op
        """
        self.assertEqual(None, self.s.scaffold())

    def test_serve_raises(self):
        """ Dummy serve() should raise """
        server = servers.Server(host="localhost", port=6786, handler=dict)
        with self.assertRaises(NotImplementedError):
            server.serve()

    def tearDown(self):
        pass


class HTTPServerTestCase(unittest.TestCase):
    def setUp(self):
        self.s = servers.HTTPServer("localhost", 8878, Handler)

    def test_close(self):
        """Close the socket"""
        mock_httpd = Mock(name='Mock HTTPD')
        self.s.httpd = mock_httpd
        self.s.close()
        mock_httpd.socket.close.assert_called_once_with()

    def test_parse_response(self):
        """ Should be a noop """
        parsed = self.s.parse_response(None, "!")
        self.assertEqual("!", parsed)


    def tearDown(self):
        pass



if __name__ == '__main__':
    unittest.main()
