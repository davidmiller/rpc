"""
Unittests for the rpc.thrifty module
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../examples/gen-py')))

import unittest

from mock import patch, Mock

from thrift.server import TProcessPoolServer
from thrift.transport import TSocket, TTransport

from service import Service
from rpc import thrifty

class ClientMakerTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_clientmaker(self):
        """ """
        c, t = thrifty._clientmaker(Service, "localhost", 567)
        self.assertIsInstance(c, Service.Client)
        self.assertIsInstance(t, TTransport.TBufferedTransport)

    def test_timeout(self):
        """ Test that the Timeout is set """
        with patch.object(TSocket.TSocket, "setTimeout") as Pset:
            c, t = thrifty._clientmaker(Service, "localhost", 666)
            Pset.assert_called_with(1000)
            c, t = thrifty._clientmaker(Service, "localhost", 666, timeout=5)
            Pset.assert_called_with(5000)

    def tearDown(self):
        pass


class ClientTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        """ Chain JSON RPC Clients"""
        client = thrifty.Client("localhost:30303", Service, timeout=0.5)
        self.assertEqual(Service, client._service)
        self.assertEqual("localhost", client.url)
        self.assertEqual(0.5, client.timeout)
        self.assertEqual(30303, client.port)
        self.assertIsInstance(client._transport, TTransport.TBufferedTransport)
        self.assertIsInstance(client._client, Service.Client)

    def test_repr(self):
        """ String Repr """
        client = thrifty.Client("localhost:30303", Service, timeout=0.5)
        self.assertEqual("<Thrift Client for localhost:30303>", str(client))

    def test_contextmanager(self):
        """ Use as a contextmanager """
        with patch.object(thrifty, 'TTransport') as Ptrans:
            with thrifty.Client("localhost:30303", Service) as c:
                self.assertIsInstance(c, Service.Client)
                Ptrans.TBufferedTransport.return_value.open.assert_called_once_with()
            Ptrans.TBufferedTransport.return_value.close.assert_called_once_with()

    def tearDown(self):
        pass

class ServerTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_repr(self):
        """ """
        server = thrifty.Server(host="localhost", port=4444, handler=dict, service=Service)
        exp = "<Thrift Server on localhost:4444 calling dict>"
        self.assertEqual(exp, str(server))

    def test_scaffold(self):
        """ Scaffold the server """
        server = thrifty.Server(host="localhost", port=4444, handler=dict, service=Service)
        self.assertIsInstance(server.handler, dict)
        self.assertIsInstance(server._server, TProcessPoolServer.TProcessPoolServer)

    def test_serve(self):
        "Serve should delegate"
        server = thrifty.Server(host="localhost", port=4444, handler=dict, service=Service)
        mock_serv = Mock(name='mock Tserver')
        server._server = mock_serv
        server.serve()
        mock_serv.serve.assert_called_once_with()

    def tearDown(self):
        pass




if __name__ == '__main__':
    unittest.main()
