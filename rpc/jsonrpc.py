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
        return lambda *a, **kw: self._apicall(self, key, *a, **kw)

    def __enter__(self):
        return self

    def __exit__(self, exc, type, stack):
        return

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

    def _apicall(self, *args, **kwargs):
        """
        Make a JSONRPC call to a JSONRPC server

        Arguments:
        - `data`: string
        """
        method = args[1]
        params = args[2:]
        reqid = uuid.uuid4().hex
        if kwargs:
            raise ValueError("Keyword arguments not supported by JSON RPC try passing a dict.")
        payload = dict(params=params, id=reqid, method=method)
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
            return result
        else:
            raise exceptions.RemoteException(result['result'])


class Server(servers.HTTPServer):
    "A JSONRPC server"
    flavour = "JSON RPC"

    def procedure(self, request):
        """
        JSON RPC procedure call - parse the params, call the procedure, and
        return the appropriate values.

        the procedure() method of HTTP Servers should return
        status, headers, content
        """
        status = '200 OK'
        headers = [('Content-Type', 'application/json')]
        result, error = None, None
        data = getattr(request, request.method)
        method, params, reqid = [json.loads(v) for v in [data.get('method', 'null'),
                                                         data.get('params', '[]'),
                                                         data.get('id', 'null')]]
        if not method:
            error = "No Method specified"
            return status, headers, dict(id=reqid, result=None, error=error)
        if not hasattr(self.handler, method):
            error = 'Method "{0}"" Not Found... '.format(method)
        if error:
            return status, headers, dict(id=id, result=result, error=error)
        try:
            result = getattr(self.handler, method)(*params)
        except Exception as err:
            error = '{error}: {msg}'.format(
                error=err.__class__.__name__, msg=err.message)
        return status, headers, dict(id=reqid, result=result, error=error)

    def parse_response(self, request, response):
        """
        Format the response:

        Just json.dump it
        """
        return json.dumps(response)
