"""
remotes.json

Provide JSONRPC and JSONP implementations
"""
import json
import uuid

import requests

from remotes import exceptions

class Client(object):
    """
    This Proxy class implements a JSONRPC API
    """

    def __init__(self, host, port, service, timeout=3):
        """
        Arguments:
        - `host`: string
        - `port`: int
        - `service`: string
        - `timeout`: number
        """
        self.url = "http://{host}:{port}/{service}".format(
            host=host, port=port, service=service)
        self.timeout = timeout

    def __repr__(self):
        return "<JSON RPC Client for {url}>".format(url=self.url)

    def __eq__(self, other):
        try:
            return self.url == other.url
        except AttributeError:
            return False

    def __getattr__(self, key):
        """
        We allow anything not in self.__dict__ to be called as a method.
        abstracting the reqests away.
        """
        if key in self.__dict__:
            return self.__dict__[key]
        return lambda **kw: self._apicall(key, **kw)

    def _apicall(self, data, *args, **kwargs):
        """
        Make a JSONRPC call to the Phase 1 JSONRPC API

        Arguments:
        - `data`: string
        """
        reqid = uuid.uuid4().hex
        payload = {'args': json.dumps(args),
                   'kwargs': json.dumps(kwargs),
                   'id': json.dumps(reqid)}
        headers = {'Content-type': 'application/json',
                   'X-flavour': 'JSONRPC'}
        resp = requests.post(
            self.url, data=payload, headers=headers, timeout=self.timeout)
        result = json.loads(resp.text)
        if reqid != result['id']:
            raise exceptions.IdError("API Endpoint returned with id:{ret}, expecting:{exp}".format(
                ret=result['id'], exp=reqid))
        del result['id']
        return result['result']
