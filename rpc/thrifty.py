"""
rpc.thrifty
"""
# import contextlib

from thrift.protocol import TBinaryProtocol
from thrift.server import TProcessPoolServer
from thrift.transport import TSocket
from thrift.transport import TTransport

from rpc import clients, servers

class ConnectionError(Exception):
    "Failed to connect to an interface with the passed params"


def _clientmaker(service, host, port, framed=False):
    "Return client instance and transport for `service'"
    transport = TSocket.TSocket(host, port)
    if framed:
        transport = TTransport.TFramedTransport(transport)
    else:
        transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = service.Client(protocol)
    return client, transport


class Client(clients.RpcProxy):
    """
    We wrap the Thrift service client in an additional layer
    to remove the need to worry about transports & protocols etc.
    """
    flavour = "Thrift"

    def __init__(self, url, service, timeout=1):
        """
        We Allow either a URI we can parse a port number from,
        or a specific port keyword argument.
        """
        self._service = service
        self.url, port = url.split(':')
        self.port = int(port)
        self.timeout = timeout
        self._client, self._transport = _clientmaker(service, self.url, self.port)

    def __repr__(self):
        return "<{flavour} Client for {url}:{port}>".format(
            url=self.url, flavour=self.flavour, port=self.port)

    def __enter__(self):
        """
        Open the transport and return the client for Thrift contextmanagers
        """
        self._transport.open()
        return self._client

    def __exit__(self, exc, type, stack):
        """
        Close the transport
        """
        self._transport.close()
        return


class Server(servers.Server):
    """
    The Thrift server instance.

    This class wraps the creation of our Thrift server in the
    Rpc API.
    """
    flavour = "Thrift"

    def __init__(self, service, **kwargs):
        """

        Arguments:
        - `service`:
        - `**kwargs`:
        """
        self.service = service
        super(Server, self).__init__(**kwargs)
        pass

    def scaffold(self):
        """
        This function is called at the end of the base class' init.
        """
        processor = self.service.Processor(self.handler)
        sockargs = {}
        if self.host:
            sockargs['port'] = self.host
        if self.port:
            sockargs['port'] = self.port
        transport = TSocket.TServerSocket(**sockargs)
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()
        self._server = TProcessPoolServer.TProcessPoolServer(processor, transport, tfactory, pfactory)
        return

    def serve(self):
        """
        Start processing incoming requests to this server
        """
        self._server.serve()



# @contextlib.contextmanager
# def Client(service, host, port, framed=False):
#     """
#     Given a Thrift service, provide a client for it.
#     """
#     client, transport = _clientmaker(service, host, port, framed=framed)
#     try:
#         transport.open()
#         yield client
#     except TTransport.TTransportException:
#         raise ConnectionError(
#             "Could not connect to {interface} on {host}:{port}".format(
#                 host=host, port=port, interface=service.__name__
#                 )
#             )
#     finally:
#         transport.close()
