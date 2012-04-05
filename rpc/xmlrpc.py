"""
This module acts as a wrapper around the standard library's xmlrpc module(s)


"""
import re
import SimpleXMLRPCServer
import urlparse
import xmlrpclib

from rpc import chains, clients, servers

def _protocolise(url):
    """
    Given a URL, check to see if there is an assocaited protocol.

    If not, set the protocol to HTTP and return the protocolised URL
    """
    # Use the regex to match http//localhost/something
    protore = re.compile(r'https?:{0,1}/{1,2}')
    parsed = urlparse.urlparse(url)
    if not parsed.scheme and not protore.search(url):
        url = 'http://{0}'.format(url)
    return url

class Client(clients.RpcProxy):
    """
    The xmlrpc.Client class wraps the Standard Library's xmlrpclib
    client, mostly for API consistency with other Rpc clients.

    >>> with Client('localhost/xmlrpc') as c:
    ...     c.ping()

    The `timeout` keyword argument specifies the per-call timeout in
    seconds.
    """
    flavour = "XML RPC"

    def __init__(self, url, timeout=3):
        """

        Arguments:
        - `url`:
        - `timeout`:
        """
        self.url = _protocolise(url)
        self.timeout = timeout
        self._proxy = xmlrpclib.ServerProxy(self.url)

    def _apicall(self, *args, **kwargs):
        """
        Call our xmlrpclib proxy
        """
        method = args[1]
        return getattr(self._proxy, method)(*args[2:], **kwargs)

def chain(*args, **kwargs ):
    """
    Will return an iterable which can be .chain()'ed as much as you
    like to create multiple Clients.

    >>> chain("localhost").chain("example.com")
    ... [<XML RPC Client for localhost>, <XML RPC Client for example.com>]
    """
    return chains.client_chain(Client, *args, **kwargs)

"""
Server Implementation
----------------------
"""
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

