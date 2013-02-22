"""
rpc.soap

The SOAP component of Rpc is mostly an API compatibility wrapper for
the excellent Suds library https://fedorahosted.org/suds/
"""
from suds.client import Client as SudsClient

from rpc import clients, urlhelp

class Client(clients.RpcProxy):
    """
    The SOAP proxy implements the client-side of a SOAP API.

    The timeout parameter specifies the ammount of time to wait for a call before
    raising an error.

    Arguments:
    - `url`: str
    - `timeout`: int

    Return: None
    Exceptions: None
    """
    flavour = "SOAP"

    def __init__(self, url, timeout=3):
        """
        Set/create instance variables
        """
        self.url = urlhelp.protocolise(url)
        self.timeout = timeout
        self._proxy = SudsClient(self.url)

    def __eq__(self, other):
        try:
            return self.url == other.url
        except AttributeError:
            return False

    def _apicall(self, *args, **kwargs):
        """
        Make a SOAP call to our server

        Return: RPC result
        Exceptions:
        - `IndecipherableResponseError`
        - `RemoteError`
        - `ConnectionError`
        """
        method = args[1]
        return getattr(self._proxy.service, method)(*args[2:], **kwargs)

