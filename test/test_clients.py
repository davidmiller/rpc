"""
Unittests for the rpc.clients module
"""
import unittest

from rpc import clients


class ClientTestCase(unittest.TestCase):

    def test_repr(self):
        """ Stringify nicely """
        client = clients.RpcProxy()
        self.assertEqual("<Base Client for None>", str(client))

    def test_contextmanager(self):
        """ Use client as a contextmanager """
        with clients.RpcProxy() as client:
            self.assertIsInstance(client, clients.RpcProxy)

    def test_getattr(self):
        """ Test the call substitution """
        client = clients.RpcProxy()
        self.assertEqual("None", client.url)
        self.assertEqual("Base", client.flavour)
        with self.assertRaises(NotImplementedError):
            client.callit(True)

    def test_apicall_nimp(self):
        """ Base apicall should raise """
        client = clients.RpcProxy()
        with self.assertRaises(NotImplementedError):
            client._apicall(False)


if __name__ == '__main__':
    unittest.main()
