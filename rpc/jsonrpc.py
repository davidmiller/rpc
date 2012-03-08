"""
rpc.jsonrpc

Provide JSONRPC implementations
"""
import json
import uuid

import requests

from rpc import exceptions, servers

class Client(object):
    """
    This Proxy class implements a JSONRPC API
    """

    def __init__(self, url, timeout=3, verb="POST"):
        """
        Arguments:
        - `url`: string
        - `timeout`: number
        - `verb`: HTTP verb to use
        """
        self.url = url
        self.timeout = timeout
        self.verb = verb

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
        return lambda *a, **kw: self._apicall(key, *a, **kw)

    def _get(self, headers, payload):
        """
        Make the call to a GET JSONRPC SERVER
        """
        return requests.get(self.url, params=payload, headers=headers,
                            timeout=self.timeout)

    def _post(self, headers, payload):
        """
        Make the call to a POST JSONRPC SERVER
        """
        return requests.post(self.url, data=payload, headers=headers,
                            timeout=self.timeout)

    def _apicall(self, method, *args, **kwargs):
        """
        Make a JSONRPC call to a JSONRPC server

        Arguments:
        - `data`: string
        """
        reqid = uuid.uuid4().hex
        payload = dict(args=args, kwargs=kwargs, method=method, id=reqid)
        payload = {k: json.dumps(v) for k, v in payload.items()}
        headers = {'X-flavour': 'JSONRPC'}
        if self.verb == "GET":
            resp = self._get(headers, payload)
        elif self.verb == "POST":
            resp = self._post(headers, payload)
        else:
            raise ValueError("Unsupported HTTP Verb {verb}".format(verb=self.verb))
        result = json.loads(resp.text)
        if reqid != result['id']:
            raise exceptions.IdError("API Endpoint returned with id:{ret}, expecting:{exp}".format(
                ret=result['id'], exp=reqid))
        del result['id']
        if resp.status_code == 200:
            return result['result']
        else:
            raise exceptions.RemoteException(result['result'])


class Server(servers.HTTPServer):
    "A JSONRPC server"
    flavour = "JSON RPC"
    def parse_response(self, request, response):
        """
        Format the response:

        Just json.dump it
        """
        return json.dumps(response)
