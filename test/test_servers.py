"""
Unittests for the rpc.servers module
"""
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from mock import patch, Mock

from rpc import servers

# Use this as our dummy handler
class Handler(object):
    def ping(self):
        return "pong!"

    def sayhi(self, person):
        return "Hi " + person

class WebobifyTestCase(unittest.TestCase):

    def test_webobify(self):
        """ Webobify the decorated function."""

        @servers.webobify
        def noop(self, request, arg):
            return request, arg

        mock_request = Mock(name='Mock Request')
        start = lambda x: x
        with patch.object(servers.webob, "Request") as Preq:
            Preq.return_value = mock_request
            req, res = noop(self, {}, start)
            self.assertEqual(start, res)
            self.assertEqual(mock_request, req)


class ServerTestCase(unittest.TestCase):
    def setUp(self):
        self.s = servers.Server(host="localhost", port=6786, handler=Handler)

    def test_initialise(self):
        """ Can we initialise?"""
        server = servers.Server(host="localhost", port=6786, handler=dict)
        self.assertEqual("localhost", server.host)
        self.assertEqual(6786, server.port)
        self.assertIsInstance(server.handler, dict)

    def test_repr(self):
        """ Test stringing """
        expected = '<Base Server on localhost:6786 calling Handler>'
        self.assertEqual(expected, str(self.s))

    def test_del(self):
        """ Should call close """
        with patch.object(self.s, 'close') as Pclose:
            self.s.__del__()
            Pclose.assert_called_once_with()

    def test_contextmanager(self):
        """ Should function as a contextmanager """
        with servers.Server(host='localhost', port=23, handler=Handler) as s:
            self.assertIsInstance(s, servers.Server)

    def test_scaffold(self):
        """
        Should be a no-op
        """
        self.assertEqual(None, self.s.scaffold())

    def test_close(self):
        """ Should be a noop """
        self.assertEqual(None, self.s.close())

    def test_procedure(self):
        "Should raise"
        with self.assertRaises(NotImplementedError):
            self.s.procedure()

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

    def test_app(self):
        """ The WSGI handler function """
        mock_procedure = Mock(name='Mock Procedure')
        mock_procedure.return_value = '200 OK', (), 'HAI'
        mock_resp = Mock(name='Mock Response')
        self.s.procedure = mock_procedure

        resp = self.s.app({}, mock_resp)
        mock_resp.assert_called_once_with('200 OK', ())
        self.assertEqual(['HAI'], resp)

    # !!! serve

    def test_procedure(self):
        "Should raise"
        with self.assertRaises(NotImplementedError):
            self.s.procedure(None)

    def tearDown(self):
        pass



if __name__ == '__main__':
    unittest.main()
