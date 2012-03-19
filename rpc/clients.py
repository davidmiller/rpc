"""
rpc.clients

Base classes for all local client proxies to inherit from.
"""

class RpcProxy(object):
    """
    A base implementation of the proxy pattern for RPC clients.
    """

    def __repr__(self):
        return "<{flavour} Client for {url}>".format(
            xurl=self.url, flavour=self.flavour)

    def __enter__(self):
        return self

    def __exit__(self, exc, type, stack):
        return

    def __getattr__(self, key):
        """
        We allow anything not in self.__dict__ to be called as a method.
        abstracting the reqests away.
        """
        if key in self.__dict__:
            return self.__dict__[key]
        return lambda *a, **kw: self._apicall(self, key, *a, **kw)

    def _apicall(self, *args, **kwargs):
        raise NotImplementedError("No proxy dispatch method!")

