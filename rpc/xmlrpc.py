"""
This module acts as a wrapper around the standard library's xmlrpc module(s)


"""
import SimpleXMLRPCServer
import xmlrpclib

from rpc import clients, servers

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
        method = args[1]
        return getattr(self._proxy, method)(*args[2:], **kwargs)


class Server(servers.Server):
    """
    An XML RPC server

    >>> with Server('localhost', 666, Handler, service=Service) as s:
    ...     s.serve()

    """
    flavour = "XML RPC"

    def scaffold(self):
        """
        Herein we construct an instance of the base stdlib server.

        As this method is implicitly called by the parent's constructor,
        there is little need for the user to call it themselves.
        """
        self._server = SimpleXMLRPCServer.SimpleXMLRPCServer((self.host, self.port))
        self._server.register_introspection_functions()
        self._server.register_instance(self.handler)
        return

    def close(self):
        """
        Frees the socket that this instance is bound to.

        This method is ensured to be called when using the server as a contextmanager,
        otherwise the user will likely want to ensure it gets closed themslves.
        """
        self._server.server_close()
        return

    def serve(self):
        """
        Begin serving XML RPC requests from this instance
        """
        self._server.serve_forever()

