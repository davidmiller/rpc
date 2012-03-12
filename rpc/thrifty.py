"""
rpc.thrifty
"""
import contextlib

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

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

@contextlib.contextmanager
def Client(service, host, port, framed=False):
    """
    Given a Thrift service, provide a client for it.
    """
    client, transport = _clientmaker(service, host, port, framed=framed)
    try:
        transport.open()
        yield client
    except TTransport.TTransportException:
        raise ConnectionError(
            "Could not connect to {{interface}} on {host}:{port}".format(
                host=host, port=port
                )
            )
    finally:
        transport.close()
