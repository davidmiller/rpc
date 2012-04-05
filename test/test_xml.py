"""
Unittests for the xmlrpc module
"""
import SimpleXMLRPCServer
import sys
import unittest
if sys.version_info < (2, 7):
    import unittest2 as unittest

from mock import patch, Mock

from rpc import xmlrpc

class Handler(object):
    def ping(self):
        return "pong!"

    def sayhi(self, person):
        return "Hi " + person

class ProtocoliseTestCase(unittest.TestCase):

    def test_leave_it_alone(self):
        """ These are already valid, leave them be"""
        cases = [
            'http://example.com',
            'https://example.com'
            ]
        for case in cases:
            self.assertEqual(case, xmlrpc._protocolise(case))

    def test_protocolise(self):
        """ Add HTTP! """
        cases = [
            ('localhost/xmlrpc',   'http://localhost/xmlrpc'),
            ('example.com', 'http://example.com')
            ]
        for case, exp in cases:
            self.assertEqual(exp, xmlrpc._protocolise(case))

    def test_typo_dont_guess(self):
        """ Probably typos don't guess though """
        cases = [
            'http//example.com',
            'http:/example.com',
            'https:example.com',
            'jttp://example.com',
            ]
        for case in cases:
            self.assertEqual(case, xmlrpc._protocolise(case))


class XmlClientTestCase(unittest.TestCase):
    def setUp(self):
        self.c = xmlrpc.Client('http://localhost/xmlrpc')

    def test_repr(self):
        """ Do we sting nicely?"""
        expected = '<XML RPC Client for http://localhost/xmlrpc>'
        self.assertEqual(expected, str(self.c))

    def test_contextmanager(self):
        """ Use WithWith """
        with xmlrpc.Client('http://localhost/xmlrpc') as c:
            self.assertIsInstance(c, xmlrpc.Client)
            self.assertEqual('http://localhost/xmlrpc', c.url)

    def test_apicall(self):
        """ Make the call to the XML RPC Proxy """
        mock_proxy = Mock(name='Mock PRoxy')
        self.c._proxy = mock_proxy
        self.c.ping()
        mock_proxy.ping.assert_called_once_with()

    def test_imply_http(self):
        """ If no protocol specified default to http """
        c = xmlrpc.Client('localhost/xmlrpc')
        self.assertEqual('http://localhost/xmlrpc', c.url)

    def tearDown(self):
        pass


class ChainTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_chain(self):
        """ Chain XML RPC Clients"""
        one, two = xmlrpc.chain("http://localhost").chain("http://example.com")
        self.assertEqual(one.url, "http://localhost")
        self.assertEqual(two.url, "http://example.com")
        for i in [one, two]:
            self.assertIsInstance(i, xmlrpc.Client)

    def tearDown(self):
        pass


class ServerTestCase(unittest.TestCase):
    def setUp(self):
        self.s = xmlrpc.Server('localhost', 6666, Handler)

    def test_repr(self):
        """ """
        exp = "<XML RPC Server on localhost:6666 calling Handler>"
        self.assertEqual(exp, str(self.s))

    def test_scaffold(self):
        """ Build the server instance """
        # scaffold is implicitly called by the base class' __init__
        self.assertIsInstance(self.s._server, SimpleXMLRPCServer.SimpleXMLRPCServer)
        # Not so sure about this, it's a little bit implementation details-y...
        self.assertEqual(('127.0.0.1', 6666), self.s._server.server_address)
        self.assertTrue(self.s._server.instance is self.s.handler)

    def test_close(self):
        """
        Do we close the socket connection on close()?
        """
        with patch.object(self.s, '_server') as Pserv:
            self.s.close()
            Pserv.server_close.assert_called_once_with()

    def test_serve(self):
        """ Delegates serving to the base """
        with patch.object(self.s._server, 'serve_forever') as Pforev:
            self.s.serve()
            Pforev.assert_called_once_with()

    def test_contextmanager(self):
        """ Can we use with with """
        with xmlrpc.Server('localhost', 5555,  Handler) as s:
            self.assertIsInstance(s, xmlrpc.Server)




    def tearDown(self):
        self.s.close()




if __name__ == '__main__':
    unittest.main()
