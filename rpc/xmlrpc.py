"""
rpc.xmlrpc

This module acts as a wrapper around the standard library's xmlrpclib module.
"""
import xmlrpclib

from rpc import clients

class Client(clients.RpcProxy):
    """
    Fairly thin wrapper for API constancy
    """
    flavour = "XML RPC"

    def __init__(self, url, timeout=3):
        """

        Arguments:
        - `url`:
        - `timeout`:
        """
        self.url = url
        self.timeout = timeout
        self._proxy = xmlrpclib.ServerProxy(url)

    def _apicall(self, *args, **kwargs):
        """
        Call our xmlrpclib proxy
        """
        raise NotImplementedError()


